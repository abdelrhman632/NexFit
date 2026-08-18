import os
import sys
import requests

from pathlib import Path
from dotenv import load_dotenv


# =========================================================
# PATHS
# =========================================================

# Current file:
# NexFit/ai-service/scripts/download_product_images.py
#
# parents[0] = scripts
# parents[1] = ai-service
# parents[2] = NexFit

AI_SERVICE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = AI_SERVICE_DIR.parent

FRONTEND_PRODUCTS_DIR = (
    PROJECT_DIR
    / "frontend"
    / "public"
    / "products"
)

FRONTEND_PRODUCTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# ENVIRONMENT
# =========================================================

ENV_FILE = AI_SERVICE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)

SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY"
)

print(
    "ENV FILE:",
    ENV_FILE
)

print(
    "ENV EXISTS:",
    ENV_FILE.exists()
)

print(
    "SERPER KEY FOUND:",
    bool(SERPER_API_KEY)
)


# =========================================================
# IMPORT EXISTING DATABASE CODE
# =========================================================

sys.path.insert(
    0,
    str(AI_SERVICE_DIR)
)

from app.database.query_executor import QueryExecutor


# =========================================================
# GET PRODUCTS FROM DATABASE
# =========================================================

def get_products():

    executor = QueryExecutor()

    sql = """
    SELECT DISTINCT
        p.productsku,
        p.productbrand,
        p.productname,
        p.productmodel
    FROM products p
    WHERE p.productsku IS NOT NULL
      AND p.productname IS NOT NULL
    ORDER BY p.productsku;
    """

    return executor.execute(sql)


# =========================================================
# SEARCH IMAGE WITH SERPER
# =========================================================

def search_image(
    brand,
    name,
    model,
):

    query_parts = []

    if brand:
        query_parts.append(
            str(brand).strip()
        )

    if name:
        query_parts.append(
            str(name).strip()
        )

    if model and model != name:
        query_parts.append(
            str(model).strip()
        )

    query_parts.extend([
        "shoe",
        "product",
    ])

    query = " ".join(
        query_parts
    )

    print(
        f"  Search: {query}"
    )

    url = (
        "https://google.serper.dev/images"
    )

    headers = {
        "X-API-KEY":
            SERPER_API_KEY,

        "Content-Type":
            "application/json",
    }

    payload = {
        "q": query,
        "num": 10,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    images = data.get(
        "images",
        []
    )

    if not images:
        return None

    for image in images:

        image_url = image.get(
            "imageUrl"
        )

        if image_url:
            return image_url

    return None


# =========================================================
# DOWNLOAD IMAGE
# =========================================================

def download_image(
    image_url,
    output_path,
):

    try:

        response = requests.get(
            image_url,
            timeout=30,
            headers={
                "User-Agent":
                    "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        content_type = (
            response.headers
            .get(
                "Content-Type",
                ""
            )
            .lower()
        )

        if not content_type.startswith(
            "image/"
        ):

            print(
                "  ✗ URL is not an image"
            )

            return False

        with open(
            output_path,
            "wb",
        ) as file:

            file.write(
                response.content
            )

        return True

    except Exception as exc:

        print(
            f"  ✗ Download error: {exc}"
        )

        return False


# =========================================================
# PROCESS PRODUCT
# =========================================================

def process_product(
    product,
    index,
    total,
):

    sku = product[
        "productsku"
    ]

    brand = product[
        "productbrand"
    ]

    name = product[
        "productname"
    ]

    model = product.get(
        "productmodel"
    )

    output_path = (
        FRONTEND_PRODUCTS_DIR
        / f"{sku}.jpg"
    )

    print()
    print(
        "-" * 60
    )

    print(
        f"[{index}/{total}] "
        f"{brand} {name}"
    )

    print(
        f"SKU: {sku}"
    )

    # -----------------------------------------------------
    # Already downloaded
    # -----------------------------------------------------

    if output_path.exists():

        print(
            "  ✓ Already exists"
        )

        return "exists"

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    try:

        image_url = search_image(
            brand,
            name,
            model,
        )

    except Exception as exc:

        print(
            f"  ✗ Search failed: {exc}"
        )

        return "failed"

    if not image_url:

        print(
            "  ✗ No image found"
        )

        return "not_found"

    print(
        "  ✓ Image found"
    )

    # -----------------------------------------------------
    # Download
    # -----------------------------------------------------

    success = download_image(
        image_url,
        output_path,
    )

    if success:

        print(
            "  ✓ Saved:"
        )

        print(
            f"    {output_path}"
        )

        return "downloaded"

    print(
        "  ✗ Download failed"
    )

    return "failed"


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print(
        "=" * 60
    )

    print(
        "NEXFIT PRODUCT IMAGE DOWNLOADER"
    )

    print(
        "=" * 60
    )

    print()

    # =====================================================
    # CHECK API KEY
    # =====================================================

    if not SERPER_API_KEY:

        raise RuntimeError(
            "SERPER_API_KEY is missing "
            "from ai-service/.env"
        )

    # =====================================================
    # LOAD PRODUCTS
    # =====================================================

    print(
        "Loading products from database..."
    )

    try:

        products = get_products()

    except Exception as exc:

        print()
        print(
            "=" * 60
        )

        print(
            "DATABASE ERROR"
        )

        print(
            "=" * 60
        )

        print(exc)

        return

    print()

    print(
        f"Found {len(products)} "
        f"products."
    )

    # =====================================================
    # STATISTICS
    # =====================================================

    results = {
        "downloaded": 0,
        "exists": 0,
        "not_found": 0,
        "failed": 0,
    }

    total = len(products)

    # =====================================================
    # DOWNLOAD ALL PRODUCTS
    # =====================================================

    for index, product in enumerate(
        products,
        start=1,
    ):

        result = process_product(
            product,
            index,
            total,
        )

        results[result] += 1

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    print()
    print(
        "=" * 60
    )

    print(
        "DOWNLOAD COMPLETE"
    )

    print(
        "=" * 60
    )

    print(
        f"Downloaded : "
        f"{results['downloaded']}"
    )

    print(
        f"Already had: "
        f"{results['exists']}"
    )

    print(
        f"Not found  : "
        f"{results['not_found']}"
    )

    print(
        f"Failed     : "
        f"{results['failed']}"
    )

    print()

    print(
        "Images directory:"
    )

    print(
        FRONTEND_PRODUCTS_DIR
    )

    print()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
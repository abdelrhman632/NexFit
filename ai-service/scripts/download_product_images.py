import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


# ============================================================
# PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent

AI_SERVICE_DIR = SCRIPT_DIR.parent

ENV_FILE = AI_SERVICE_DIR / ".env"

# Change this if your images are stored somewhere else.
IMAGE_DIR = AI_SERVICE_DIR / "product_images"

IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ENV
# ============================================================

load_dotenv(ENV_FILE)

SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY"
)

if not SERPER_API_KEY:
    raise RuntimeError(
        f"SERPER_API_KEY not found in:\n{ENV_FILE}"
    )


# ============================================================
# ONLY THE REMAINING 9
# ============================================================

PRODUCTS = [
    "SK-GW6-101",
    "BK-AW2-101",
    "NK-SRG3-101",
    "PM-FUS2-101",
    "NB-OUT-101",
    "NK-THR-101",
    "CV-C70-101",
    "CV-RSH-101",
    "AD-PRA1-101",
    "AD-TSR3-101",
]


# ============================================================
# SERPER
# ============================================================

SERPER_URL = "https://google.serper.dev/images"

HEADERS = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json",
}


# ============================================================
# HELPERS
# ============================================================

def clean_filename(value: str) -> str:
    """
    Make sure the SKU is safe as a Windows filename.
    """

    return re.sub(
        r'[<>:"/\\|?*]',
        "_",
        value,
    )


def search_images(sku: str):
    """
    Search Google Images through Serper.
    """

    queries = [
        f'"{sku}" shoe',
        f'"{sku}" sneakers',
        sku,
    ]

    for query in queries:

        print(
            f"    Searching: {query}"
        )

        try:

            response = requests.post(
                SERPER_URL,
                headers=HEADERS,
                json={
                    "q": query,
                    "num": 10,
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            images = data.get(
                "images",
                []
            )

            if images:
                return images

        except Exception as exc:

            print(
                f"    Search failed: {exc}"
            )

    return []


def download_image(
    image_url: str,
    output_path: Path,
) -> bool:

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

        content_type = response.headers.get(
            "Content-Type",
            "",
        ).lower()

        if not content_type.startswith(
            "image/"
        ):
            return False

        if len(response.content) < 5000:
            return False

        output_path.write_bytes(
            response.content
        )

        return True

    except Exception as exc:

        print(
            f"    Download failed: {exc}"
        )

        return False


# ============================================================
# DOWNLOAD ONE PRODUCT
# ============================================================

def download_product(
    sku: str,
) -> bool:

    filename = (
        clean_filename(sku)
        + ".jpg"
    )

    output_path = (
        IMAGE_DIR / filename
    )

    print()
    print("=" * 60)
    print(f"PRODUCT: {sku}")
    print("=" * 60)

    # --------------------------------------------------------
    # Already exists
    # --------------------------------------------------------

    if output_path.exists():

        print(
            f"Already exists: {output_path}"
        )

        return True

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    images = search_images(
        sku
    )

    if not images:

        print(
            "    ❌ No images found"
        )

        return False

    print(
        f"    Found {len(images)} image results"
    )

    # --------------------------------------------------------
    # Try images one by one
    # --------------------------------------------------------

    for index, image in enumerate(
        images,
        start=1,
    ):

        image_url = image.get(
            "imageUrl"
        )

        if not image_url:
            continue

        print(
            f"    Trying image {index}..."
        )

        success = download_image(
            image_url,
            output_path,
        )

        if success:

            print(
                f"    ✅ Downloaded:"
                f" {output_path.name}"
            )

            return True

    print(
        "    ❌ All image downloads failed"
    )

    return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print(
        "NEXFIT — REMAINING PRODUCT IMAGE DOWNLOADER"
    )
    print("=" * 60)

    print(
        f"ENV: {ENV_FILE}"
    )

    print(
        f"IMAGE DIRECTORY: {IMAGE_DIR}"
    )

    print(
        f"Products remaining: {len(PRODUCTS)}"
    )

    print()

    downloaded = 0
    already_exists = 0
    failed = 0

    for sku in PRODUCTS:

        output_path = (
            IMAGE_DIR
            / f"{clean_filename(sku)}.jpg"
        )

        if output_path.exists():

            already_exists += 1

            print(
                f"✓ Already exists: {sku}"
            )

            continue

        success = download_product(
            sku
        )

        if success:
            downloaded += 1
        else:
            failed += 1

        # Avoid hammering Serper
        time.sleep(1)

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)

    print(
        f"Downloaded    : {downloaded}"
    )

    print(
        f"Already had   : {already_exists}"
    )

    print(
        f"Failed        : {failed}"
    )

    print(
        f"Total checked : {len(PRODUCTS)}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
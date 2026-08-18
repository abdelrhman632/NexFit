from app.services.product_search import ProductSearchService


def main():

    print("=" * 60)
    print("TESTING FULL PRODUCT DATA")
    print("=" * 60)

    data = {
        "needs_database": True,
        "filters": {
            "gender": ["Men", "Unisex"],
            "category": "Running",
            "usage": None,
            "size": 42,
            "max_price": 10000,
            "min_price": None,
            "branch": "Nasr City Branch",
        },
    }

    service = ProductSearchService()

    result = service.search(data)

    products = result.get(
        "products",
        [],
    )

    print(
        f"\nFound {len(products)} candidate products."
    )

    required_fields = [
        "productid",
        "sku",
        "productname",
        "productbrand",
        "productmodel",
        "productprice",
        "productgender",
        "productcategory",
        "productusage",
        "productsize",

        # Full recommendation attributes
        "material",
        "surface",
        "supporttype",
        "cushioning",
        "breathability",
        "weight",
        "waterproof",
        "description",
        "recommendeddistance",
        "archtype",
        "footstrike",
        "energyreturn",
        "releaseyear",
        "heeldropmm",
        "terrain",

        # Inventory
        "branches",
    ]

    for index, product in enumerate(
        products,
        start=1,
    ):

        print("=" * 60)
        print(f"PRODUCT {index}")
        print("=" * 60)

        print(
            f"Name: {product.get('productname')}"
        )

        print(
            f"SKU: {product.get('sku')}"
        )

        print("\nFIELDS:")

        missing = []

        for field in required_fields:

            value = product.get(field)

            print(
                f"  {field}: {value}"
            )

            if value is None:
                missing.append(field)

        print("\nSTATUS:")

        if missing:
            print(
                "MISSING FIELDS:"
            )

            for field in missing:
                print(
                    f"  - {field}"
                )

        else:
            print(
                "FULL PRODUCT DATA AVAILABLE"
            )


if __name__ == "__main__":
    main()
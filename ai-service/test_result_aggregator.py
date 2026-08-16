from app.services.result_aggregator import ResultAggregator


def main():

    rows = [
        {
            "productid": 49,
            "productname": "Skechers Max Road 6",
            "productbrand": "Skechers",
            "productmodel": "Max Road 6",
            "productprice": 5800,
            "productgender": "Unisex",
            "productcategory": "Running",
            "productusage": "Long Distance",
            "productsize": 42,
            "quantity": 1,
            "branchname": "New Cairo Branch",
            "city": "Cairo",
        },
        {
            "productid": 49,
            "productname": "Skechers Max Road 6",
            "productbrand": "Skechers",
            "productmodel": "Max Road 6",
            "productprice": 5800,
            "productgender": "Unisex",
            "productcategory": "Running",
            "productusage": "Long Distance",
            "productsize": 42,
            "quantity": 2,
            "branchname": "Rehab Branch",
            "city": "Cairo",
        },
        {
            "productid": 49,
            "productname": "Skechers Max Road 6",
            "productbrand": "Skechers",
            "productmodel": "Max Road 6",
            "productprice": 5800,
            "productgender": "Unisex",
            "productcategory": "Running",
            "productusage": "Long Distance",
            "productsize": 42,
            "quantity": 1,
            "branchname": "Zamalek Branch",
            "city": "Cairo",
        },
    ]

    aggregator = ResultAggregator()

    results = aggregator.aggregate(rows)

    print("=" * 60)
    print("AGGREGATED RESULTS")
    print("=" * 60)

    for product in results:

        print()
        print(product["productname"])
        print("Price:", product["productprice"])
        print("Size:", product["productsize"])

        print("Branches:")

        for branch in product["branches"]:

            print(
                f"  - {branch['branchname']} "
                f"({branch['city']}) "
                f"Quantity: {branch['quantity']}"
            )


if __name__ == "__main__":
    main()
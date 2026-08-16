from collections import OrderedDict


class ResultAggregator:

    def aggregate(self, rows: list[dict]) -> list[dict]:

        products = OrderedDict()

        for row in rows:

            product_id = row["productid"]

            if product_id not in products:

                products[product_id] = {
                    "productid": product_id,
                    "sku": row["productsku"],
                    "productname": row["productname"],
                    "productbrand": row["productbrand"],
                    "productmodel": row["productmodel"],
                    "productprice": row["productprice"],
                    "productgender": row["productgender"],
                    "productcategory": row["productcategory"],
                    "productusage": row["productusage"],
                    "productsize": row["productsize"],
                    "branches": [],
                }

            products[product_id]["branches"].append({
                "branchname": row["branchname"],
                "city": row["city"],
                "quantity": row["quantity"],
            })

        return list(products.values())
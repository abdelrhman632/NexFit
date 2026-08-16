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
                    "material": row["productmaterial"],
                    "surface": row["productsurface"],
                    "supporttype": row["productsupporttype"],
                    "cushioning": row["productcushioning"],
                    "breathability": row["productbreathability"],
                    "weight": row["productweight"],
                    "waterproof": row["productwaterproof"],
                    "description": row["productdescription"],
                    "recommendeddistance": row["recommendeddistance"],
                    "archtype": row["archtype"],
                    "footstrike": row["footstrike"],
                    "energyreturn": row["energyreturn"],
                    "releaseyear": row["releaseyear"],
                    "heeldropmm": row["heeldropmm"],
                    "terrain": row["terrain"],
                }

            products[product_id]["branches"].append({
                "branchname": row["branchname"],
                "city": row["city"],
                "quantity": row["quantity"],
            })

        return list(products.values())
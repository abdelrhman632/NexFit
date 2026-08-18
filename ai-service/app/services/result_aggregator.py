from collections import OrderedDict


class ResultAggregator:

    def aggregate(
        self,
        rows: list[dict],
    ) -> list[dict]:

        products = OrderedDict()

        for row in rows:

            product_id = row["productid"]

            # =================================================
            # CREATE PRODUCT
            # =================================================

            if product_id not in products:

                products[product_id] = {

                    "productid":
                        product_id,

                    "sku":
                        row["productsku"],

                    "productname":
                        row["productname"],

                    "productbrand":
                        row["productbrand"],

                    "productmodel":
                        row["productmodel"],

                    "productprice":
                        row["productprice"],

                    "productgender":
                        row["productgender"],

                    "productcategory":
                        row["productcategory"],

                    "productusage":
                        row["productusage"],

                    "productsize":
                       row["productsize"],

                    # -----------------------------------------
                    # FULL PRODUCT ATTRIBUTES
                    # -----------------------------------------

                    "material":
                        row["productmaterial"],

                    "surface":
                        row["productsurface"],

                    "supporttype":
                        row["productsupporttype"],

                    "cushioning":
                        row["productcushioning"],

                    "breathability":
                        row["productbreathability"],

                    "weight":
                        row["productweight"],

                    "waterproof":
                        row["productwaterproof"],

                    "description":
                        row["productdescription"],

                    "recommendeddistance":
                        row["recommendeddistance"],

                    "archtype":
                        row["archtype"],

                    "footstrike":
                        row["footstrike"],

                    "energyreturn":
                        row["energyreturn"],

                    "releaseyear":
                        row["releaseyear"],

                    "heeldropmm":
                        row["heeldropmm"],

                    "terrain":
                        row["terrain"],

                    # -----------------------------------------
                    # BRANCHES
                    # -----------------------------------------

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

            product = products[product_id]

            # =================================================
            # INVENTORY INFORMATION
            # =================================================

            branch_name = row["branchname"]
            city = row["city"]
            size = row["productsize"]
            quantity = row["quantity"]

            # =================================================
            # FIND EXISTING BRANCH
            # =================================================

            existing_branch = None

            for branch in product["branches"]:

                if (
                    branch["branchname"]
                    == branch_name
                    and
                    branch["city"]
                    == city
                ):

                    existing_branch = branch
                    break

            # =================================================
            # CREATE BRANCH
            # =================================================

            if existing_branch is None:

                product["branches"].append({

                    "branchname":
                        branch_name,

                    "city":
                        city,

                    "quantity":
                        quantity,

                    "sizes": [
                        {
                            "size": size,
                            "quantity": quantity,
                        }
                    ],
                })

                continue

            # =================================================
            # EXISTING BRANCH
            # =================================================

            existing_size = None

            for size_data in existing_branch["sizes"]:

                if (
                    size_data["size"]
                    == size
                ):

                    existing_size = size_data
                    break

            # =================================================
            # ADD NEW SIZE
            # =================================================

            if existing_size is None:

                existing_branch["sizes"].append({

                    "size":
                        size,

                    "quantity":
                        quantity,
                })

            # =================================================
            # SAME SIZE
            # =================================================

            else:

                existing_size["quantity"] += quantity

            # =================================================
            # UPDATE TOTAL BRANCH QUANTITY
            # =================================================

            existing_branch["quantity"] = sum(
                item["quantity"]
                for item
                in existing_branch["sizes"]
            )

        return list(
            products.values()
        )
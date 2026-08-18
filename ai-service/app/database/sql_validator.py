import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
    "products": {
        "productid",
        "productsku",
        "productname",
        "productbrand",
        "productmodel",
        "productcategory",
        "productgender",
        "productprice",
        "productmaterial",
        "productusage",
        "productsurface",
        "productsupporttype",
        "productcushioning",
        "productbreathability",
        "productweight",
        "productwaterproof",
        "productdescription",
        "recommendeddistance",
        "archtype",
        "footstrike",
        "energyreturn",
        "releaseyear",
        "heeldropmm",
        "terrain",
    },

    "storeinventory": {
        "inventoryid",
        "branchid",
        "productid",
        "productsize",
        "productcolor",
        "quantity",
        "lastupdated",
    },

    "branches": {
        "branchid",
        "branchname",
        "city",
        "address",
        "phone",
        "openinghours",
        "isactive",
    },
}


def validate_sql(sql: str) -> tuple[bool, str]:

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    try:
        statements = sqlglot.parse(sql, read="postgres")
    except Exception as exc:
        return False, f"Invalid SQL syntax: {exc}"

    if len(statements) != 1:
        return False, "Only one SQL statement is allowed."

    statement = statements[0]

    if not isinstance(statement, exp.Select):
        return False, "Only SELECT statements are allowed."

    # ---------------------------------------------------------
    # Build table + alias map
    # ---------------------------------------------------------

    tables = statement.find_all(exp.Table)

    table_aliases = {}

    for table in tables:
        table_name = table.name.lower()

        if table_name not in ALLOWED_TABLES:
            return False, f"Table '{table_name}' is not allowed."

        # Actual table name can always reference itself
        table_aliases[table_name] = table_name

        # If an alias exists, map alias -> actual table
        alias = table.alias

        if alias:
            table_aliases[alias.lower()] = table_name

    # ---------------------------------------------------------
    # Validate columns
    # ---------------------------------------------------------

    for column in statement.find_all(exp.Column):

        column_name = column.name.lower()
        table_reference = column.table.lower()

        # -----------------------------------------------------
        # Qualified column:
        # p.productid
        # -----------------------------------------------------

        if table_reference:

            if table_reference not in table_aliases:
                return False, (
                    f"Column '{column_name}' references "
                    f"unknown table or alias '{table_reference}'."
                )

            actual_table = table_aliases[table_reference]

            if column_name not in ALLOWED_TABLES[actual_table]:
                return False, (
                    f"Column '{column_name}' is not allowed "
                    f"for table '{actual_table}'."
                )

        # -----------------------------------------------------
        # Unqualified column:
        # productid
        # -----------------------------------------------------

        else:

            matching_tables = [
                table_name
                for table_name, columns in ALLOWED_TABLES.items()
                if column_name in columns
            ]

            if not matching_tables:
                return False, (
                    f"Column '{column_name}' is not allowed."
                )

            if len(matching_tables) > 1:
                return False, (
                    f"Column '{column_name}' is ambiguous. "
                    f"Use a table name or alias."
                )

    return True, "SQL is valid."
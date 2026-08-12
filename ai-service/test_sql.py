from app.services.llm import LLMService


def main():

    llm = LLMService()

    request = """
أريد حذاء جري للرجال مقاس 42، مناسب للمسافات الطويلة،
وسعره أقل من 7000 جنيه، ويكون متوفراً في فرع مدينة نصر.
"""

    result = llm.generate_sql(request)

    print("=" * 50)
    print("GENERATED SQL")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    main()
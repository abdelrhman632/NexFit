from app.services.llm import LLMService


def main():

    llm = LLMService()

    response = llm.generate_response(
        "أريد حذاء جري مريح للمسافات الطويلة."
    )

    print("=" * 50)
    print("GEMINI RESPONSE")
    print("=" * 50)
    print(response)


if __name__ == "__main__":
    main()
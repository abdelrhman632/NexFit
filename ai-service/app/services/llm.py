import os

from google import genai

from app.prompts.system_prompt import NEXFIT_SYSTEM_PROMPT
from app.prompts.sql_prompt import NEXFIT_SQL_SYSTEM_PROMPT
from app.prompts.recommendation_prompt import (
    RECOMMENDATION_SYSTEM_PROMPT,
)


MODEL_NAME = "gemini-3.6-flash"


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not configured."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

    # =========================================================
    # GENERAL AI RESPONSE
    # =========================================================

    def generate_response(self, user_text: str) -> str:

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=NEXFIT_SYSTEM_PROMPT,
            ),
        )

        return response.text

    # =========================================================
    # SQL GENERATION
    # =========================================================

    def generate_sql(self, user_text: str) -> str:

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=NEXFIT_SQL_SYSTEM_PROMPT,
            ),
        )

        return response.text

    # =========================================================
    # RECOMMENDATION PREFERENCE GENERATION
    # =========================================================

    def generate_recommendation_preferences(
        self,
        user_text: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=RECOMMENDATION_SYSTEM_PROMPT,
                response_mime_type="application/json",
            ),
        )

        return response.text
from google import genai

from app.prompts.system_prompt import NEXFIT_SYSTEM_PROMPT
from app.prompts.sql_prompt import NEXFIT_SQL_SYSTEM_PROMPT

MODEL_NAME = "gemini-3.6-flash"


class LLMService:

    def __init__(self):
        self.client = genai.Client(
            enterprise=True,
            project="project-8e81b4ea-c0d9-4fcf-a60",
            location="global",
        )

    def generate_response(self, user_text: str) -> str:

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=NEXFIT_SYSTEM_PROMPT,
            ),
        )

        return response.text

    def generate_sql(self, user_text: str) -> str:

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=user_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=NEXFIT_SQL_SYSTEM_PROMPT,
            ),
        )

        return response.text
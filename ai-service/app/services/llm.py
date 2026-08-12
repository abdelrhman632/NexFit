from google import genai

from app.prompts.system_prompt import NEXFIT_SYSTEM_PROMPT


MODEL_NAME = "gemini-3.6-flash"


class LLMService:

    def __init__(self):
        self.client = genai.Client(
            enterprise=True,
            project="YOUR_PROJECT_ID",
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
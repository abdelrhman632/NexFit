import os
import requests

from app.prompts.system_prompt import NEXFIT_SYSTEM_PROMPT
from app.prompts.sql_prompt import NEXFIT_SQL_SYSTEM_PROMPT
from app.prompts.recommendation_prompt import (
    RECOMMENDATION_SYSTEM_PROMPT,
)


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Good general-purpose model for the application.
MODEL_NAME = "openai/gpt-5.5"


class LLMService:

    def __init__(self):

        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY environment variable is not configured."
            )

        self.api_key = api_key

    # =========================================================
    # INTERNAL OPENROUTER REQUEST
    # =========================================================

    def _generate(
        self,
        user_text: str,
        system_prompt: str,
        json_mode: bool = False,
    ) -> str:

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_text,
                },
            ],
        }

        if json_mode:
            payload["response_format"] = {
                "type": "json_object"
            }

        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nexfit-production-738b.up.railway.app",
                "X-Title": "NexFit",
            },
            json=payload,
            timeout=120,
        )

        # Give us the actual OpenRouter error instead of
        # hiding it behind a generic 500.
        if not response.ok:
            raise RuntimeError(
                f"OpenRouter API error "
                f"{response.status_code}: {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected OpenRouter response: {data}"
            ) from exc

    # =========================================================
    # GENERAL AI RESPONSE
    # =========================================================

    def generate_response(self, user_text: str) -> str:

        return self._generate(
            user_text=user_text,
            system_prompt=NEXFIT_SYSTEM_PROMPT,
        )

    # =========================================================
    # SQL GENERATION
    # =========================================================

    def generate_sql(self, user_text: str) -> str:

        return self._generate(
            user_text=user_text,
            system_prompt=NEXFIT_SQL_SYSTEM_PROMPT,
        )

    # =========================================================
    # RECOMMENDATION PREFERENCE GENERATION
    # =========================================================

    def generate_recommendation_preferences(
        self,
        user_text: str,
    ) -> str:

        return self._generate(
            user_text=user_text,
            system_prompt=RECOMMENDATION_SYSTEM_PROMPT,
            json_mode=True,
        )
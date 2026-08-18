import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.llm import LLMService
from app.services.product_search import ProductSearchService


app = FastAPI(
    title="NexFit AI API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str


llm = LLMService()
search_service = ProductSearchService()


def parse_gemini_json(response_text: str) -> dict:

    text = response_text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return json.loads(text)


@app.get("/")
def root():

    return {
        "message": "NexFit AI API is running"
    }


@app.post("/api/search")
def search_products(request: SearchRequest):

    try:

        # Gemini → structured search filters
        response = llm.generate_sql(
            request.query
        )

        data = parse_gemini_json(response)

        # Structured filters → database search
        result = search_service.search(data)

        return result

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os

class FactCheckInput(BaseModel):
    statement: str = Field(..., description="The statement to verify.")

class FactCheckerTool(BaseTool):
    name: str = "Fact Checker"
    description: str = "Verifies the accuracy of a given statement using Bing News (via RapidAPI)."
    args_schema: Type[BaseModel] = FactCheckInput

    def _run(self, statement: str) -> str:
        api_key = os.getenv("RAPIDAPI_KEY") 
        if not api_key:
            return "Error: Please set RAPIDAPI_KEY in your environment."

        url = "https://bing-news-seZarch1.p.rapidapi.com/news/search"
        headers = {
            "x-bingapis-sdk": "true",
            "x-rapidapi-host": "bing-news-search1.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
        params = {
            "q": statement,
            "safeSearch": "Off",
            "textFormat": "Raw"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if "value" not in data or not data["value"]:
                return f"No reliable news sources found for: {statement}"

            results = [
                f"- {item['name']} ({item['provider'][0]['name']}): {item['url']}"
                for item in data["value"][:3]
            ]
            return f"Fact-check results for '{statement}':\n" + "\n".join(results)

        except Exception as e:
            return f"Error during fact-checking: {e}"

import os
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class SummarizerInput(BaseModel):
    text: str = Field(..., description="The text to summarize.")

class SummarizerTool(BaseTool):
    name: str = "Summarizer"
    description: str = "Summarizes long text into concise bullet points or paragraphs."
    args_schema: Type[BaseModel] = SummarizerInput

    def _run(self, text: str) -> str:
        api_key = os.getenv("HF_API_KEY")
        if not api_key:
            return "Error: HuggingFace API key not set (HF_API_KEY)."

        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"inputs": text}
        )
        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        return "Summary:\n" + response.json()[0]["summary_text"]

import os
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class WriterInput(BaseModel):
    content: str = Field(..., description="The structured summary to turn into a detailed report.")

class WriterTool(BaseTool):
    name: str = "Report Writer"
    description: str = "Converts structured content into a professional, markdown-formatted report."
    args_schema: Type[BaseModel] = WriterInput

    def _run(self, content: str) -> str:
        api_key = os.getenv("HF_API_KEY")
        if not api_key:
            return "Error: Please set HF_API_KEY in your environment."

        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "inputs": f"Turn the following structured notes into a professional markdown report:\n\n{content}"
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        report = response.json()[0]["generated_text"]
        return f"# Research Report\n\n{report}\n\n---\n_End of Report_"

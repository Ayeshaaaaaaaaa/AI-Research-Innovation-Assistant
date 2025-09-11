from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr
import language_tool_python


class ReviewerInput(BaseModel):
    report: str = Field(..., description="The full report to review.")


class ReviewerTool(BaseTool):
    # declare private attributes so Pydantic doesn't treat them as model fields
    _tool: language_tool_python.LanguageTool = PrivateAttr()

    def __init__(self):
        super().__init__(
            name="Report Reviewer",
            description="Reviews the report for grammar, clarity, and formatting.",
            args_schema=ReviewerInput
        )
        # assign to private attr
        self._tool = language_tool_python.LanguageTool('en-US')

    def _run(self, report: str) -> str:
        # use private attribute
        matches = self._tool.check(report)
        corrected_text = language_tool_python.utils.correct(report, matches)

        suggestions = [f"- {m.ruleId}: {m.message}" for m in matches[:5]]
        suggestions_text = "\n".join(suggestions) if suggestions else "No major issues found."

        return (
            f"✅ Reviewed Report:\n\n"
            f"{corrected_text}\n\n"
            f"---\n"
            f"**Suggestions:**\n{suggestions_text}"
        )

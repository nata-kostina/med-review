import json
from typing import Any

from pydantic import ValidationError

from app.correction_email.base import CorrectionEmailDrafter, CorrectionEmailDraftingError
from app.correction_email.schemas import CorrectionEmailDraft
from app.documents.schemas import ReviewData, ValidationIssue


class AzureOpenAICorrectionEmailDrafter(CorrectionEmailDrafter):
    def __init__(
        self, 
        *, 
        client: Any, 
        deployment_name: str,
        sender_name: str = "Anna Smirnova",
        sender_role: str = "Laboratory Requisition Specialist",
        company_name: str = "LabTest Diagnostics",
    ) -> None:
        self.client = client
        self.deployment_name = deployment_name
        self.instructions = f"""
Draft a concise, professional correction-request email to the referring clinic or doctor regarding an incoming patient document.
Mention only the provided medical facts and identified discrepancies (e.g., missing or invalid patient name, date of birth, ordering physician, diagnosis).
Do not mention AI, OCR, extraction confidence, internal automation tools, or invent contact details.
Ask for a corrected lab requisition form or explicit written clarification so the sample can be processed.
Use a neutral, respectful greeting and sign off as {sender_name}, {sender_role}, {company_name}.
""".strip()  # noqa: E501

    def draft(
        self, data: ReviewData, issues: list[ValidationIssue]
    ) -> CorrectionEmailDraft:
        payload = json.dumps(
            {
                "document": data.model_dump(mode="json"),
                "issues": [issue.model_dump(mode="json") for issue in issues],
            }
        )
        try:
            response = self.client.responses.create(
                model=self.deployment_name,
                instructions=self.instructions,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": payload,
                            }
                        ],
                    }
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "correction_email_draft",
                        "strict": True,
                        "schema": CorrectionEmailDraft.model_json_schema(),
                    }
                },
            )
        except Exception as error:
            raise CorrectionEmailDraftingError(
                "Azure OpenAI could not draft the correction email."
            ) from error

        try:
            return CorrectionEmailDraft.model_validate(json.loads(response.output_text))
        except (json.JSONDecodeError, ValidationError, TypeError) as error:
            raise CorrectionEmailDraftingError(
                "Azure OpenAI returned an invalid correction-email draft."
            ) from error

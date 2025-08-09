from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Decision(BaseModel):
    chosen_option: str
    reason: str

    model_config: ConfigDict = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": {
                "chosen_option": "Galaxy Samsung S25",
                "reason": "Since you prefer the best zoom performance in photography, the Samsung Galaxy S25 is the most suitable choice.",  # noqa: E501
            },
        },
    )


class DecisionRequest(BaseModel):
    user_id: UUID
    question_answer_pairs: list[dict[str, str]]

    model_config: ConfigDict = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": {
                "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "question_answer_pairs": [
                    {
                        "question": "What matters more for your photography experience?",
                        "answer": "Full manual control and advanced shooting modes",
                    },
                    {
                        "question": "When choosing a phone, what's more important?",
                        "answer": "Hardware features and higher camera specs",
                    },
                ],
            },
        },
    )

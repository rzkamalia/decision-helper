from pydantic import BaseModel, ConfigDict
from typing_extensions import TypedDict


class Question(BaseModel):
    question: str
    answer_choices: list[str]

    model_config: ConfigDict = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": {
                "question": "When choosing a phone, what's more important?",
                "answer_choices": [
                    "Long-term software support and ecosystem integration",
                    "Hardware features and higher camera specs",
                ],
            },
        },
    )


class Questions(BaseModel):
    questions: list[Question]

    model_config: ConfigDict = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": [
                {
                    "question": "What matters more for your photography experience?",
                    "answer_choices": [
                        "Simpler camera with consistent automatic results",
                        "Full manual control and advanced shooting modes",
                    ],
                },
                {
                    "question": "When choosing a phone, what's more important?",
                    "answer_choices": [
                        "Long-term software support and ecosystem integration",
                        "Hardware features and higher camera specs",
                    ],
                },
            ],
        },
    )


class QuestionGeneratorState(TypedDict):
    context: str
    options: list[str]
    web_search: str
    questions: Questions


class QuestionRequest(BaseModel):
    context: str
    options: list[str]

    model_config: ConfigDict = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": {
                "context": "Best HP for photography.",
                "options": [
                    "Iphone 16",
                    "Samsung S25",
                ],
            },
        },
    )

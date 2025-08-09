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
    user_id: str
    context: str
    options: list[str]
    question_answer_pairs: list[dict[str, str]]
    image_content: list[str]
    web_search_content: str

    model_config: ConfigDict = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": {
                "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "context": "Best HP for photography.",
                "options": [
                    "Iphone 16",
                    "Samsung S25",
                ],
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
                "image_content": [
                    "The image shows a stylish, dark brown leather handbag with a textured finish. It has two short handles and a long adjustable shoulder strap attached with gold hardware. The handbag features clean lines and appears to have a structured shape. The brand name 'TOSCAN' is printed in gold near the bottom center of the bag. The background is plain white, highlighting the handbag.",  # noqa: E501
                    "The image shows a green handbag with two handles. The bag has a textured surface and features gold-colored hardware where the handles attach to the bag. There is also a small gold logo or text near the bottom center that reads 'TOSCO TOSCANO.' The overall design of the bag is simple and elegant.",  # noqa: E501
                ],
                "web_search_content": "Regarding the best phones for photography between the iPhone 16 and Samsung Galaxy S25:\n\niPhone 16:\n- The iPhone 16 Pro and Pro Max are highly praised for capturing everyday moments beautifully with accurate and natural photos.\n- It offers advanced photographic control, zero shutter lag, and cinematic-quality 4K video recording up to 120fps.\n- The iPhone 16 Pro is recommended for those who prefer accurate colors and photos that edit well with software.\n- Some critiques mention the macro performance and low-light selfie camera could be improved.\n\nSamsung Galaxy S25:\n- The Galaxy S25 Ultra is considered the best all-round Android camera phone with multiple high-resolution sensors and advanced AI editing features.\n- It produces vibrant, dramatic photos with excellent dynamic range and versatile camera modes.\n- The S25 Ultra has a 50MP ultra-wide lens and five cameras optimized for detailed and vibrant photos in various settings.\n- It is favored by influencers and those who want impressive, colorful images straight out of the camera.\n\nSummary:\n- iPhone 16 Pro is best for natural, accurate photos and professional video recording.\n- Samsung Galaxy S25 Ultra excels in vibrant, versatile photography with powerful AI editing tools.\n\nYour choice depends on whether you prioritize natural accuracy and video quality (iPhone 16) or vibrant, versatile photos with AI enhancements (Samsung S25).",  # noqa: E501
            },
        },
    )

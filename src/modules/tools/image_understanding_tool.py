from openai import OpenAI

client = OpenAI()


def image_understanding(base64_image: str) -> str:
    """Image understanding"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "What's in this image?"},
                        {
                            "type": "input_image",
                            "image_url": f"{base64_image}",
                        },
                    ],
                }
            ],
        )

        return response.output_text
    except Exception as e:
        print(f"Image understanding failed: {e}")
        return ""

import json

import requests
from agents import function_tool

from src import app_config


@function_tool
def image_understanding(image_base64: str) -> str:
    """Image understanding using vision language model."""
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {app_config.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>",  # optional
                "X-Title": "<YOUR_SITE_NAME>",  # optional
            },
            data=json.dumps(
                {
                    "model": "qwen/qwen2.5-vl-72b-instruct:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "What is in this image?"},
                                {"type": "image_url", "image_url": {"url": image_base64}},
                            ],
                        }
                    ],
                }
            ),
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        return f"[HTTP error] {e.response.status_code}: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"[Request failed] {e!s}"
    except KeyError:
        return "[Error] Unexpected response format"
    except Exception as e:
        return f"[Unexpected error] {e!s}"

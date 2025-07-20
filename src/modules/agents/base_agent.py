from langchain_openai import ChatOpenAI


class BaseAgent:
    def __init__(self):
        pass

    def get_llm(self):
        llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0.1,
            max_tokens=None,
            timeout=None,
            max_retries=3,
        )
        return llm

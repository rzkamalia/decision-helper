import os

from src.cores.config import Configuration

app_config = Configuration()

os.environ["OPENAI_API_KEY"] = app_config.openai_api_key
os.environ["TAVILY_API_KEY"] = app_config.tavily_api_key
os.environ["LANGCHAIN_TRACING_V2"] = app_config.langchain_tracing_v2
os.environ["LANGSMITH_API_KEY"] = app_config.langsmith_api_key
os.environ["LANGSMITH_PROJECT"] = app_config.langsmith_project


from datetime import datetime, timedelta

from agents import function_tool
from exa_py import Exa

from src import app_config

current_date = (datetime.now() - timedelta(days=365)).date().isoformat()


@function_tool
def web_search(query: str) -> str:
    """Web searching using Exa with a given query."""
    try:
        exa = Exa(api_key=app_config.exa_api_key)

        result = exa.search_and_contents(
            query,
            type="keyword",
            num_results=1,
            summary=True,
        )
        return result
    except Exception as e:
        print(f"Web search failed: {e}")
        return ""

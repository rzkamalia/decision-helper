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
            num_results=2,
            summary=True,
            start_crawl_date=current_date,
        )
        
        result_str = ""
        for i, res in enumerate(result.results, start=1):
            result_str += f"## Website {i}\n"
            result_str += f"### Title: {res.title}\n"
            result_str += f"### URL: {res.url}\n"
            result_str += f"### Content: {res.summary}\n"
            result_str += "\n"

        return result_str
    except Exception as e:
        print(f"Web search failed: {e}")
        return ""

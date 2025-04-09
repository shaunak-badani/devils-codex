# pip3 install -U duckduckgo-search
from langchain_community.tools import DuckDuckGoSearchRun

class WebSearchTool:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()

    def run(self, query: str) -> str:
        # Limit results and restrict to duke.edu
        results = self.search_tool.run(f"{query} site:duke.edu", num_results=5)
        if isinstance(results, str):
            return results  # fallback for single string result

        formatted = "\n".join(
            [f"{i+1}. {res['title']} - {res['href']}" for i, res in enumerate(results)]
        )
        return f"Top search results:\n{formatted}"

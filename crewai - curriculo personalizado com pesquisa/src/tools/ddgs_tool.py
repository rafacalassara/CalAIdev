from crewai.tools import BaseTool
from duckduckgo_search import DDGS
from typing import Type
from pydantic import BaseModel, Field

class DuckDuckGoSearchInput(BaseModel):
    """Schema de entrada para a ferramenta de busca"""
    query: str = Field(..., description="A consulta de busca a ser executada")

class DuckDuckGoSearchTool(BaseTool):
    name: str = "Internet Search"
    description: str = (
        "Search the internet for information using DuckDuckGo. "
        "Use this tool FIRST to search for company information, news, articles, and any data you need. "
        "This is your primary tool for researching companies, finding their websites, social media, and public information. "
        "Always use this tool before trying to scrape websites."
    )
    args_schema: Type[BaseModel] = DuckDuckGoSearchInput

    def _run(self, query: str) -> str:
        """Executa a busca no DuckDuckGo"""
        ddgs = DDGS()
        results = ddgs.text(
            keywords=query,
            region='wt-wt',
            safesearch='moderate',
            timelimit=None,
            max_results=10
        )
        
        if not results:
            return "Nenhum resultado encontrado."

        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   Descrição: {result['body']}\n"
            )
        
        return "\n".join(formatted_results)

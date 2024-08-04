import os
from typing import List, Literal, Optional

import requests
from pydantic import Field
from rich.console import Console

from atomic_agents.agents.base_agent import BaseIOSchema
from atomic_agents.lib.tools.base_tool import BaseTool, BaseToolConfig


################
# INPUT SCHEMA #
################
class SearxNGToolInputSchema(BaseIOSchema):
    """
    Schema for input to a tool for searching for information, news, references, and other content using SearxNG.
    Returns a list of search results with a short description or content snippet and URLs for further exploration
    """

    queries: List[str] = Field(..., description="List of search queries.")
    category: Optional[Literal["general", "news", "social_media"]] = Field(
        "general", description="Category of the search queries."
    )


####################
# OUTPUT SCHEMA(S) #
####################
class SearxNGSearchResultItemSchema(BaseIOSchema):
    """This schema represents a single seaarch result item"""

    url: str = Field(..., description="The URL of the search result")
    title: str = Field(..., description="The title of the search result")
    content: Optional[str] = Field(None, description="The content snippet of the search result")


class SearxNGToolOutputSchema(BaseIOSchema):
    """This schema represents the output of the SearxNG search tool."""

    results: List[SearxNGSearchResultItemSchema] = Field(..., description="List of search result items")
    category: Optional[str] = Field(None, description="The category of the search results")


##############
# TOOL LOGIC #
##############
class SearxNGToolConfig(BaseToolConfig):
    base_url: str = ""
    max_results: int = 10


class SearxNGTool(BaseTool):
    """
    Tool for performing searches on SearxNG based on the provided queries and category.

    Attributes:
        input_schema (SearxNGToolInputSchema): The schema for the input data.
        output_schema (SearxNGToolOutputSchema): The schema for the output data.
        max_results (int): The maximum number of search results to return.
        base_url (str): The base URL for the SearxNG instance to use.
    """

    input_schema = SearxNGToolInputSchema
    output_schema = SearxNGToolOutputSchema

    def __init__(self, config: SearxNGToolConfig = SearxNGToolConfig()):
        """
        Initializes the SearxNGTool.

        Args:
            config (SearxNGToolConfig):
                Configuration for the tool, including base URL, max results, and optional title and description overrides.
        """
        super().__init__(config)
        self.base_url = config.base_url
        self.max_results = config.max_results

    def run(self, params: SearxNGToolInputSchema, max_results: Optional[int] = None) -> SearxNGToolOutputSchema:
        """
        Runs the SearxNGTool with the given parameters.

        Args:
            params (SearxNGToolInputSchema): The input parameters for the tool, adhering to the input schema.
            max_results (Optional[int]): The maximum number of search results to return.

        Returns:
            SearxNGToolOutputSchema: The output of the tool, adhering to the output schema.

        Raises:
            ValueError: If the base URL is not provided.
            Exception: If the request to SearxNG fails.
        """
        all_results = []

        for query in params.queries:
            # Prepare the query parameters
            query_params = {
                "q": query,
                "safesearch": "0",
                "format": "json",
                "language": "en",
                "engines": "bing,duckduckgo,google,startpage,yandex",
            }

            # Add category to query parameters if it is set
            if params.category:
                query_params["categories"] = params.category

            # Make the GET request
            response = requests.get(f"{self.base_url}/search", params=query_params)

            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(
                    f"Failed to fetch search results for query '{query}': {response.status_code} {response.reason}"
                )

            results = response.json().get("results", [])
            all_results.extend(results)

        # Sort the combined results by score in descending order
        sorted_results = sorted(all_results, key=lambda x: x.get("score", 0), reverse=True)

        # Remove duplicates while preserving order
        seen_urls = set()
        unique_results = []
        for result in sorted_results:
            if "content" not in result or "title" not in result or "url" not in result:
                continue
            if result["url"] not in seen_urls:
                unique_results.append(result)
                if "metadata" in result:
                    result["title"] = f"{result['title']} - (Published {result['metadata']})"
                if "publishedDate" in result and result["publishedDate"]:
                    result["title"] = f"{result['title']} - (Published {result['publishedDate']})"
                seen_urls.add(result["url"])

        # Filter results to include only those with the correct category if it is set
        if params.category:
            filtered_results = [result for result in unique_results if result.get("category") == params.category]
        else:
            filtered_results = unique_results

        filtered_results = filtered_results[: max_results or self.max_results]

        return SearxNGToolOutputSchema(results=filtered_results, category=params.category)


#################
# EXAMPLE USAGE #
#################
if __name__ == "__main__":
    rich_console = Console()
    search_tool_instance = SearxNGTool(config=SearxNGToolConfig(base_url=os.getenv("SEARXNG_BASE_URL"), max_results=5))

    search_input = SearxNGTool.input_schema(
        queries=["Python programming", "Machine learning", "Artificial intelligence"],
        category="news",
    )

    output = search_tool_instance.run(search_input)

    rich_console.print(output)

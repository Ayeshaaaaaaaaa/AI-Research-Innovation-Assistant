from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from scholarly import scholarly
import time

class SearchScholarInput(BaseModel):
    query: str = Field(..., description="Search query for academic publications")

class SearchScholar(BaseTool):
    name: str = "Scholar Search"
    description: str = "Fetch academic publication titles from Google Scholar for a given query."
    args_schema: Type[BaseModel] = SearchScholarInput

    def _run(self, query: str) -> str:
        try:
            # Add a delay to avoid rate limiting
            time.sleep(1)
            
            search_gen = scholarly.search_pubs(query)
            results = []
            
            for _ in range(3):  # get top 3 results
                try:
                    pub = next(search_gen)
                    bib = pub.get("bib", {})
                    title = bib.get("title", "No title")
                    author = bib.get("author", "Unknown authors")
                    year = bib.get("pub_year", "N/A")
                    results.append(f"{title} ({year}) - {author}")
                except StopIteration:
                    break  # No more results
                except Exception as e:
                    return f"Error processing result: {e}"
            
            if not results:
                return "No results found for the query."
            
            return "Top results:\n• " + "\n• ".join(results)
            
        except Exception as e:
            # Return a clear error message but don't raise an exception
            return f"Search failed: {str(e)}. Please try again with a different query."
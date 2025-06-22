from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from datetime import datetime
import wikipedia

# -----------------------------
# Save Tool (No Changes Needed)
# -----------------------------
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

# -----------------------------
# DuckDuckGo Search Tool
# -----------------------------
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information. Input should be a search query string.",
)

# -----------------------------
# Custom Wikipedia Tool (Returns URLs)
# -----------------------------
def wiki_lookup(query: str) -> str:
    """Returns the Wikipedia URL for the query topic."""
    try:
        page = wikipedia.page(query)
        return page.url
    except Exception as e:
        return f"❌ Wikipedia error: {e}"

wiki_tool = Tool(
    name="wiki",
    func=wiki_lookup,
    description="Get the Wikipedia URL for a topic"
)

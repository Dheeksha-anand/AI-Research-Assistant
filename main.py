# backend/main.py

from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional  # ✅ added for Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .tools import search_tool, wiki_tool, save_tool

# Load environment variables
load_dotenv()

# ✅ Define the expected output structure
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: Optional[List[str]] = []  # ✅ Made optional with default

# Initialize the Groq LLM
llm = ChatGroq(model="llama3-70b-8192")  # Requires GROQ_API_KEY in .env

# Define the output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a research assistant helping generate research summaries using available tools.

You can call tools when needed. Only reply in JSON using this format:
{format_instructions}

Instructions:
- Choose a relevant topic from the query.
- Use tools (search, wiki, save) if helpful.
- Populate all fields: topic, summary, and sources (as full URLs).
- Avoid including "tools_used" in the final output.
- Don't return plain text; return only JSON.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Define available tools
tools = [search_tool, wiki_tool, save_tool]

# Create agent with tools
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Executor to run agent logic
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Export for FastAPI to use
__all__ = ["agent_executor", "parser"]

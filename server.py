# backend/server.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.main import agent_executor, parser

# Initialize FastAPI app
app = FastAPI()

# CORS configuration to allow requests from frontend (localhost:5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Recommended: ["http://127.0.0.1:5500"] for strict CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class QueryRequest(BaseModel):
    query: str

# POST endpoint for frontend to send queries
@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        raw_response = agent_executor.invoke({"query": request.query})
        output = raw_response.get("output", "")
        if output:
            structured = parser.parse(output)
            return {
                "success": True,
                "topic": structured.topic,
                "summary": structured.summary,
                "sources": structured.sources
            }
        else:
            return {"success": False, "error": "Empty response."}
    except Exception as e:
        return {"success": False, "error": str(e)}

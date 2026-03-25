from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Input Schema: What Next.js sends to FastAPI
class AnalysisRequest(BaseModel):
    content: str = Field(..., min_length=10, description="The raw journal text to analyze")

# 2. Output Schema: The "Neural" data structure the AI must return
# This matches the JSON format we told Ollama to use
class AnalysisResult(BaseModel):
    sentiment: float = Field(..., ge=0, le=1, description="Sentiment score from 0 to 1")
    topics: List[str] = Field(default_factory=list, description="List of extracted keywords")
    cognitive_load: str = Field(..., description="Mental energy level: low, medium, or high")
    summary: str = Field(..., max_length=150, description="A one-sentence abstract of the entry")

# 3. Response Schema: What the API returns to Next.js immediately
class TaskResponse(BaseModel):
    message: str
    task_id: str
    status: str = "queued"
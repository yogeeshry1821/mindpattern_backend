from fastapi import APIRouter
from .tasks import analyze_entry_task
from .schemas import AnalysisRequest

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])

@router.post("/analyze/{journal_id}")
async def trigger_analysis(journal_id: str, data: AnalysisRequest):
    # This is non-blocking. It pushes to Redis and returns immediately.
    task = analyze_entry_task.delay(journal_id, data.content)
    return {"message": "Analysis queued", "task_id": task.id}
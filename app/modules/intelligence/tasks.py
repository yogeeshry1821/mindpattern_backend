from app.core.celery_app import celery_app
from .services import call_ollama_analysis
import json

@celery_app.task(name="analyze_entry_task")
def analyze_entry_task(journal_id: str, content: str):
    # 1. Get the AI results
    raw_analysis = call_ollama_analysis(content)
    analysis_json = json.loads(raw_analysis)
    
    # 2. Logic to update your PostgreSQL Database here
    # (We can use psycopg2 or Prisma-Python in the next step)
    print(f"COMMITTING ANALYSIS TO DB FOR {journal_id}")
    return {"journal_id": journal_id, "status": "completed"}
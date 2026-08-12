from app.core.celery_app import celery_app
from .services import call_ollama_analysis
from app.core.database import update_journal_analysis
import json
import logging

logger = logging.getLogger(__name__)

@celery_app.task(
    name="analyze_entry_task",
    bind=True,
    max_retries=2,
    default_retry_delay=5,  # seconds between retries
)
def analyze_entry_task(self, journal_id: str, content: str):
    try:
        # 1. Get the AI results
        raw_analysis = call_ollama_analysis(content)
        analysis_dict = json.loads(raw_analysis)

        # 2. Update PostgreSQL
        update_journal_analysis(journal_id, analysis_dict)
        return {"journal_id": journal_id, "status": "completed"}

    except (ValueError, json.JSONDecodeError) as e:
        # Malformed output from the model - retry, model may succeed on a second pass
        logger.warning(f"Analysis parse failure for journal {journal_id}, attempt {self.request.retries + 1}: {e}")
        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            logger.error(f"Analysis permanently failed for journal {journal_id} after {self.max_retries} retries")
            update_journal_analysis(journal_id, {"error": "analysis_failed", "detail": str(e)})
            return {"journal_id": journal_id, "status": "failed"}
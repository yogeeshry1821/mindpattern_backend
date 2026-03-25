# app/modules/intelligence/__init__.py

from .router import router
from .tasks import analyze_entry_task

# Now in main.py, you can just do:
# from app.modules.intelligence import router
# app/core/celery_app.py
from celery import Celery

# 'localhost' works because we mapped the Docker port to your host machine
REDIS_URL = "redis://localhost:6379/0"

celery_app = Celery(
    "mindpattern",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.modules.intelligence.tasks"] 
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_concurrency=1, # Save that 16GB RAM!
)
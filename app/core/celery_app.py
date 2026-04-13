# app/core/celery_app.py
from celery import Celery
import os
# 'localhost' works because we mapped the Docker port to your host machine

# Use the env var, default to the docker service name 'redis'
broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "mindpattern",
    broker=broker_url,
    backend=broker_url
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_concurrency=1, # Save that 16GB RAM!
)
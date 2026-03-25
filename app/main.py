from fastapi import FastAPI
from app.modules.intelligence.router import router as intelligence_router

app = FastAPI(title="MindPattern Neural Engine")

# This is where we "stitch" the feature into the main app
app.include_router(intelligence_router)

@app.get("/")
async def root():
    return {"status": "Neural Engine Online", "version": "2026.1"}
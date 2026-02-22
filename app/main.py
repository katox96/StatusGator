import asyncio
from fastapi import FastAPI

from .api.routes import router
from .watcher import watcher

app = FastAPI(title="StatusGator")

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(watcher())


@app.get("/health")
def health():
    return {"status": "ok"}
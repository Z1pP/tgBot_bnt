import uvicorn
from fastapi import FastAPI

from app.api.v1 import base_router as api_router
from app.database.config import engine
from app.models.base import Base

app = FastAPI(docs_url="/docs", root_path="/api")
app.include_router(api_router)


@app.on_event("startup")
async def initialize_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/root", operation_id="health_status")
async def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

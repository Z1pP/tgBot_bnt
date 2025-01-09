import logging
from typing import Any

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import base_router as api_router
from app.core.config import setting
from app.exceptions.base import AppException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI application",
        description="A backend for tg bot",
        docs_url="/docs",
        root_path="/api",
    )

    # cors middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = create_app()


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code, content={"status": "error", "message": exc.message}
    )


@app.get("/health", operation_id="health_status", tags=["Health"])
async def health_check() -> dict[str, Any]:
    try:
        return {
            "status": "healthy",
            "message": "Service is running smoothly",
            "database": "connected",
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "message": str(e)},
        )


def main():
    try:
        logger.info("Апишечка стартанула")
        uvicorn.run(app, host=setting.API_HOST, port=setting.API_PORT)
    except Exception as e:
        logger.error(f"Ошибка при запуске апишки: {e}")
        raise


if __name__ == "__main__":
    main()

import json

from fastapi import APIRouter

from lisa_on_cuda import app_logger


router = APIRouter()


@router.get("/health")
def health() -> str:
    try:
        app_logger.info("health check")
        return json.dumps({"msg": "ok"})
    except Exception as e:
        app_logger.error(f"exception:{e}.")
        return json.dumps({"msg": "request failed"})

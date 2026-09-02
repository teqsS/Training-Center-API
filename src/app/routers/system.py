from fastapi import APIRouter

system_info = {
    "name": "training_center_api",
    "version": "0.1.0",
    "status": "is running",
}

router = APIRouter(
    tags=["System"],
)


@router.get(
    "/",
    status_code=200,
    summary="Get service name, version, and status",
)
async def check_system():
    return system_info

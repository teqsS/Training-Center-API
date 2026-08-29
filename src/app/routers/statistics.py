from fastapi import APIRouter

from app.schemas import *

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


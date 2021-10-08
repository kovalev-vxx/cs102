from api.routers import router as other_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(other_router)

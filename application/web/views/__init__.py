from fastapi import APIRouter
from .user.routers import router as router_user
from .category_ad.routers import router as router_category_ad
from .ad.routers import router as router_ad
from .moderation.routers import router as router_moderation

router = APIRouter()
router.include_router(router=router_user)
router.include_router(router=router_category_ad)
router.include_router(router=router_ad)
router.include_router(router=router_moderation)

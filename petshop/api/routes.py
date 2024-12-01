from fastapi import APIRouter
from api.routes_app.firms import router as firm_router
from api.routes_app.coupon import router as coupon_router
from api.routes_app.animals import router as animals_router
from api.routes_app.roles import router as role_router
from api.routes_app.category_goods import router as category_good_router
from api.routes_app.users import router as app_router
from api.routes_app.carts import router as cart_router
from api.routes_app.goods import router as good_router
from api.routes_app.orders import router as order_router
from api.routes_app.logs import router as log_router
from api.routes_app.auth import router as auth_router




def get_apps_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth_router, prefix="/auth", tags=["auth"])
    router.include_router(log_router, prefix="/logs", tags=["logs"])
    router.include_router(order_router, prefix="/orders", tags=["orders"])
    router.include_router(good_router, prefix="/goods", tags=["goods"])
    router.include_router(cart_router, prefix="/carts", tags=["carts"])
    router.include_router(category_good_router, prefix="/categories", tags=["categories"])
    router.include_router(role_router, prefix="/roles", tags=["roles"])
    router.include_router(coupon_router, prefix="/coupons", tags=["coupons"])
    router.include_router(firm_router, prefix="/firms", tags=["firms"])
    router.include_router(animals_router, prefix="/animals", tags=["animals"])
    router.include_router(app_router, prefix="/users", tags=["users"])
    return router
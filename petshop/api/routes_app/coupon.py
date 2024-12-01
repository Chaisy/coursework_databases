from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_admin_user, get_current_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import CouponCreate, Coupon

router = APIRouter()

@router.get("/coupons", response_model=List[dict])
async def get_all_coupons(current_admin: TokenData = Depends(get_current_user)):
    
    coupons = await DatabaseQueries.get_all_coupons()

    if not coupons:
        raise HTTPException(status_code=404, detail="No coupons found")

    return coupons

@router.get("/coupons/{coupon_id}", response_model=dict)
async def get_coupon_by_id(coupon_id: UUID,
                           current_admin: TokenData = Depends(get_current_user)):
    coupon = await DatabaseQueries.get_coupon(coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon

@router.post("/coupons", response_model=Coupon)
async def create_coupon(coupon: CouponCreate,
                        current_admin: TokenData = Depends(get_admin_user)):
    if not coupon.sale:
        raise HTTPException(status_code=400, detail="Naming field must be filled")

    coupon_data = await DatabaseQueries.create_coupon(coupon.sale)

    if not coupon_data:
        raise HTTPException(status_code=500, detail="Coupon could not be created")

    return coupon_data


@router.delete("/coupons/{coupon_id}", response_model=dict)
async def delete_coupon_by_id(coupon_id: UUID,
                              current_admin: TokenData = Depends(get_admin_user)):
    is_deleted = await DatabaseQueries.delete_coupon(coupon_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Coupon not found or could not be deleted")
    return {"message": f"Coupon with ID {coupon_id} has been deleted."}



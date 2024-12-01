from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_current_user, get_admin_user
from config.database.queries_table import DatabaseQueries
router = APIRouter()




@router.get("/orders", response_model=List[dict])
async def get_all_orders(current_admin: TokenData = Depends(get_admin_user)):
    return await DatabaseQueries.get_all_orders()



@router.get("/orders/user/{user_id}", response_model=List[dict])
async def get_orders_by_user_id(user_id: UUID, current_admin: TokenData = Depends(get_admin_user)):
    return await DatabaseQueries.get_orders_by_user_id(user_id)



@router.get("/orders/{order_id}/goods", response_model=List[UUID])
async def get_order_goods(order_id: UUID, current_admin: TokenData = Depends(get_current_user)):
    goods = await DatabaseQueries.get_order_goods(order_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Order not found or no goods")
    return goods


@router.put("/orders/user/{user_id}/goods/{good_id}", response_model=dict)
async def add_good_to_order(user_id: UUID, good_id: UUID,
                            current_admin: TokenData = Depends(get_current_user)):
    order = await DatabaseQueries.add_good_to_order(user_id, good_id)
    if not order:
        raise HTTPException(status_code=500, detail="Failed to add good to order")
    return order



@router.delete("/orders/{order_id}/goods/{good_id}", response_model=dict)
async def remove_good_from_order(order_id: UUID, good_id: UUID, current_admin: TokenData = Depends(get_current_user)):
    result = await DatabaseQueries.remove_good_from_order(order_id, good_id)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to remove good from order")
    return result



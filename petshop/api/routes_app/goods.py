from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from api.auth.token import TokenData
from api.routes_app.auth import get_current_user, get_admin_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import GoodCreate, GoodUpdate, Good

router = APIRouter()

@router.get("/", response_model=List[Good])
async def get_all_goods():
    goods = await DatabaseQueries.get_all_goods()
    if goods:
        return goods
    raise HTTPException(status_code=404, detail="Goods not found")

@router.get("/{good_id}", response_model=Good)
async def get_good_by_id(good_id: UUID,
                         ):
    good = await DatabaseQueries.get_good_by_id(good_id)
    if good:
        return good
    raise HTTPException(status_code=404, detail="Good not found")

@router.post("/", response_model=Good)
async def add_good(good: GoodCreate,
                   current_admin: TokenData = Depends(get_admin_user)):
    new_good = await DatabaseQueries.add_good(good)
    if new_good:
        return new_good
    raise HTTPException(status_code=400, detail="Error creating good")

@router.delete("/{good_id}", response_model=dict)
async def delete_good(good_id: UUID,
                      current_admin: TokenData = Depends(get_admin_user)):
    success = await DatabaseQueries.delete_good(good_id)
    if success:
        return {"message": "Good deleted successfully"}
    raise HTTPException(status_code=404, detail="Good not found")

@router.patch("/{good_id}", response_model=Good)
async def update_good(good_id: UUID, good_update: GoodUpdate,
                      current_admin: TokenData = Depends(get_admin_user)):
    updated_good = await DatabaseQueries.update_good(good_id, good_update)
    if updated_good:
        return updated_good
    raise HTTPException(status_code=400, detail="Error updating good")


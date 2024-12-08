from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_admin_user, get_current_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import CategoryCreate, Category

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_all_categories():
    
    categories = await DatabaseQueries.get_all_categories()

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return categories

@router.get("/{category_id}", response_model=dict)
async def get_category_by_id(category_id: UUID,
                             ):
    category = await DatabaseQueries.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=Category)
async def create_category(category: CategoryCreate,
                          current_admin: TokenData = Depends(get_admin_user)):
    if not category.title:
        raise HTTPException(status_code=400, detail="Naming field must be filled")

    category_data = await DatabaseQueries.create_category(category.title)

    if not category_data:
        raise HTTPException(status_code=500, detail="Category could not be created")

    return category_data


@router.delete("/{category_id}", response_model=dict)
async def delete_category_by_id(category_id: UUID,
                                current_admin: TokenData = Depends(get_admin_user)):
    is_deleted = await DatabaseQueries.delete_category(category_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Category not found or could not be deleted")
    return {"message": f"Category with ID {category_id} has been deleted."}



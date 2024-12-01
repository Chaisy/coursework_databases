from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_admin_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import User, UserProfile, UserUpdate, UserCreate
from config.project_config import Database


router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_users(current_admin: TokenData = Depends(get_admin_user)):
    users = await DatabaseQueries.get_users()  # Получаем всех пользователей из БД
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")  # Возвращаем ошибку, если пользователей нет
    return users

@router.get("/user/{user_id}", response_model=dict)
async def get_user_profile_by_id(user_id: UUID,
                                 current_admin: TokenData = Depends(get_admin_user)):
    user_profile = await DatabaseQueries.get_user_profile(user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found")
    return user_profile


@router.patch("/user/{user_id}", response_model=dict)
async def update_user_profile(user_id: UUID, user_update: UserUpdate, current_admin: TokenData = Depends(get_admin_user)):
    # Преобразуем данные из схемы в обычный словарь
    update_data = user_update.dict(exclude_unset=True)

    # Вызываем метод для обновления данных пользователя
    success = await DatabaseQueries.update_user(user_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="This data is already exists")

    # Возвращаем обновленные данные
    updated_user = await DatabaseQueries.get_user_profile(user_id)
    return updated_user

@router.delete("/user/{user_id}", response_model=dict)
async def delete_user_by_id(user_id: UUID, current_admin: TokenData = Depends(get_admin_user)):
    is_deleted = await DatabaseQueries.delete_user(user_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="User not found or could not be deleted")
    return {"message": f"User with ID {user_id} has been deleted."}




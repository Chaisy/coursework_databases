from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List


from api.auth.token import TokenData
from api.routes_app.auth import get_admin_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import Cart, CartItemUpdate, LogResponse, LogCreate

router = APIRouter()

@router.get("/", response_model=List[LogResponse])
async def get_logs(current_admin: TokenData = Depends(get_admin_user)):
    logs = await DatabaseQueries.get_logging()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")
    return logs


@router.get("/{user_id}", response_model=List[LogResponse])
async def get_logs_by_user(user_id: UUID,
                           current_admin: TokenData = Depends(get_admin_user)):
    logs = await DatabaseQueries.get_logging_by_user(user_id)
    if not logs:
        raise HTTPException(status_code=404, detail=f"No logs found for user {user_id}")
    return logs


@router.post("/logs", response_model=LogResponse)
async def create_log(log: LogCreate,
                     current_admin: TokenData = Depends(get_admin_user)):
    new_log = await DatabaseQueries.add_log(log)
    if not new_log:
        raise HTTPException(status_code=500, detail="Failed to create log")
    return new_log






from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_admin_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import RoleCreate, Role

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_all_roles(current_admin: TokenData = Depends(get_admin_user)):
    
    roles = await DatabaseQueries.get_all_roles()

    if not roles:
        raise HTTPException(status_code=404, detail="No roles found")

    return roles

@router.get("/{role_id}", response_model=dict)
async def get_role_by_id(role_id: UUID):
    role = await DatabaseQueries.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/", response_model=Role)
async def create_role(role: RoleCreate, current_admin: TokenData = Depends(get_admin_user)):
    if not role.name:
        raise HTTPException(status_code=400, detail="Naming field must be filled")

    role_data = await DatabaseQueries.create_role(role.name)

    if not role_data:
        raise HTTPException(status_code=500, detail="Role could not be created")

    return role_data


@router.delete("/{role_id}", response_model=dict)
async def delete_role_by_id(role_id: UUID,
                            current_admin: TokenData = Depends(get_admin_user)):
    is_deleted = await DatabaseQueries.delete_role(role_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Role not found or could not be deleted")
    return {"message": f"Role with ID {role_id} has been deleted."}



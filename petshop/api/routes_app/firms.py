from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List

from api.auth.token import TokenData
from api.routes_app.auth import get_admin_user, get_current_user
from config.database.queries_table import DatabaseQueries
from schemas.schemas import FirmCreate, Firm

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_all_firms():
    
    firms = await DatabaseQueries.get_all_firms()

    if not firms:
        raise HTTPException(status_code=404, detail="No firms found")

    return firms

@router.get("/firms/{firm_id}", response_model=dict)
async def get_firm_by_id(firm_id: UUID,
                         ):
    firm = await DatabaseQueries.get_firm(firm_id)
    if not firm:
        raise HTTPException(status_code=404, detail="Firm not found")
    return firm

@router.post("/", response_model=Firm)
async def create_firm(firm: FirmCreate,
                      current_admin: TokenData = Depends(get_admin_user)):
    if not firm.naming:
        raise HTTPException(status_code=400, detail="Naming field must be filled")

    firm_data = await DatabaseQueries.create_firm(firm.naming)

    if not firm_data:
        raise HTTPException(status_code=500, detail="Firm could not be created")

    return firm_data


@router.delete("/{firm_id}", response_model=dict)
async def delete_firm_by_id(firm_id: UUID,
                            current_admin: TokenData = Depends(get_admin_user)):
    is_deleted = await DatabaseQueries.delete_firm(firm_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Firm not found or could not be deleted")
    return {"message": f"Firm with ID {firm_id} has been deleted."}



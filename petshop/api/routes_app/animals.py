from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from pydantic import BaseModel
from api.routes_app.auth import get_admin_user, get_current_user
from api.auth.token import TokenData
from config.database.queries_table import DatabaseQueries
from schemas.schemas import AnimalCreate



class Animal(BaseModel):
    id: UUID
    type: str

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/", response_model=List[Animal])
async def get_all_animals():
    try:
        
        animals = await DatabaseQueries.get_all_animals()

        
        formatted_animals = [{"id": row["id"], "type": row["type"]} for row in animals]

        if not formatted_animals:
            raise HTTPException(status_code=404, detail="No animals found")

        return formatted_animals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/{animal_id}", response_model=dict)
async def get_animal_by_id(animal_id: UUID,
                           ):
    animal = await DatabaseQueries.get_animal(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.post("/", response_model=Animal)
async def create_animal(animal: AnimalCreate,
                        current_admin: TokenData = Depends(get_admin_user)):
    if not animal.type:
        raise HTTPException(status_code=400, detail="Type field must be filled")

    
    animal_data = await DatabaseQueries.create_animal(animal.type)
    print("Animal Data:", animal_data)  

    if not animal_data:
        raise HTTPException(status_code=500, detail="Animal could not be created")

    return animal_data

@router.delete("/{animal_id}", response_model=dict)
async def delete_animal_by_id(
    animal_id: UUID,
    current_admin: TokenData = Depends(get_admin_user)  
):
    
    is_deleted = await DatabaseQueries.delete_animal(animal_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Animal not found or could not be deleted")
    return {"message": f"Animal with ID {animal_id} has been deleted."}


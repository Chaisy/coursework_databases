from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from fastapi import Request
from api.auth.token import (
    decode_access_token,
    Token,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TokenData,
    blacklist_token,
)
from config.database.queries_table import DatabaseQueries
from schemas.schemas import LoginRequest, UserProfile, UserUpdate, UserCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        
        token_data = decode_access_token(token)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_admin_user(token: str = Depends(oauth2_scheme)):

        token_data = decode_access_token(token)
        user_id = token_data.user_id

        
        user = await DatabaseQueries.get_user_profile(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        
        role_id = user["roleid"]
        role = await DatabaseQueries.get_role_by_id(role_id)

        if not role or role != "admin":  
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: Admin only")

        return token_data  

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    
    user = await DatabaseQueries.get_user_by_login(login_request.username)

    
    if not user or login_request.password != user["password"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    
    if user["banned"]:
        raise HTTPException(status_code=403, detail="User is banned")

    
    token_data = {
        "user_id": str(user["id"]),
        "role": str(user["roleId"]),
    }

    
    access_token = create_access_token(token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    
    blacklist_token(token)
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserProfile)
async def get_me(current_user: TokenData = Depends(get_current_user)):
    user_id = current_user.user_id
    user = await DatabaseQueries.get_user_profile(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserProfile(
        id=user["id"],
        login=user["login"],
        name=user["name"],
        roleid=user["roleid"],
        couponId=user.get("couponid"),
        banned=user["banned"]
    )


@router.patch("/me", response_model=dict)
async def update_user_profile(
    request:Request,
    user_update: UserUpdate = Body(...),
    current_user: TokenData = Depends(get_current_user),
):
    user_id = current_user.user_id

    update_data = user_update.dict(exclude_unset=True)

    
    success = await DatabaseQueries.update_user(user_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="This data is already exists")

    
    updated_user = await DatabaseQueries.get_user_profile(user_id)
    return updated_user


@router.post("/register", response_model=UserProfile)
async def create_user(user: UserCreate):
    
    if not user.login or not user.password or not user.name:
        raise HTTPException(status_code=400, detail="All fields must be filled")

    
    user_data = await DatabaseQueries.create_user(user.login, user.password, user.name)

    
    if not user_data:
        raise HTTPException(status_code=400, detail="User could not be created")

    
    return user_data
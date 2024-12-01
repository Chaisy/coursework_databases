from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

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
        # Декодируем токен и извлекаем информацию
        token_data = decode_access_token(token)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_admin_user(token: str = Depends(oauth2_scheme)):

        token_data = decode_access_token(token)
        user_id = token_data.user_id

        # Получаем информацию о пользователе
        user = await DatabaseQueries.get_user_profile(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        print(user)

        # Проверяем роль пользователя через таблицу Roles
        role_id = user["roleid"]
        print(role_id)
        role = await DatabaseQueries.get_role_by_id(role_id)
        print(role)

        if not role or role != "admin":  # Проверяем, что роль называется "admin"
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: Admin only")

        return token_data  # Возвращаем информацию о пользователе

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    # Получаем пользователя из базы данных
    user = await DatabaseQueries.get_user_by_login(login_request.username)

    # Проверяем, существует ли пользователь и совпадает ли пароль
    if not user or login_request.password != user["password"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Если пользователь забанен
    if user["banned"]:
        raise HTTPException(status_code=403, detail="User is banned")

    # Создаём данные для токена
    token_data = {
        "user_id": str(user["id"]),
        "role": str(user["roleId"]),
    }

    # Генерируем access token
    access_token = create_access_token(token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # Возвращаем токен
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Добавляем токен в черный список
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


@router.patch("/user/me", response_model=dict)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
):
    user_id = current_user.user_id  # Берем ID из токена

    # Преобразуем данные из схемы в словарь, исключая незаданные поля
    update_data = user_update.dict(exclude_unset=True)

    # Вызываем метод для обновления данных пользователя
    success = await DatabaseQueries.update_user(user_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="This data is already exists")

    # Возвращаем обновленные данные
    updated_user = await DatabaseQueries.get_user_profile(user_id)
    return updated_user


@router.post("/register", response_model=UserProfile)
async def create_user(user: UserCreate):
    # Проверка, что все обязательные поля заполнены
    if not user.login or not user.password or not user.name:
        raise HTTPException(status_code=400, detail="All fields must be filled")

    # Пытаемся создать пользователя в базе данных
    user_data = await DatabaseQueries.create_user(user.login, user.password, user.name)

    # Если пользователь не был создан, выбрасываем ошибку
    if not user_data:
        raise HTTPException(status_code=400, detail="User could not be created")

    # Преобразуем данные в UserProfile и возвращаем
    return user_data
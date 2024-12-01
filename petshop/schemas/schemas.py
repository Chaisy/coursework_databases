from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional, List

from pydantic import BaseModel


class LogCreate(BaseModel):
    userid: Optional[UUID] = None
    role: Optional[str] = None
    action: str
    result: Optional[str] = None

class LogResponse(LogCreate):
    id: UUID
    timestamp: datetime

class OrderItemUpdate(BaseModel):
    cart_id: UUID
    good_id: UUID

class Order(BaseModel):
    id: UUID  
    userId: UUID  
    goods: List[UUID] = []  

    class Config:
        from_attributes = True
        alias_generator = lambda name: name.lower()


class GoodBase(BaseModel):
    title: str
    firmId: UUID
    categoryOfGoodId: UUID
    animalId: UUID
    price: float

class GoodCreate(GoodBase):
    class Config:
        from_attributes = True
        alias_generator = lambda name: name.lower()

class GoodUpdate(BaseModel):
    title: Optional[str] = None
    firmId: Optional[UUID] = None
    categoryOfGoodId: Optional[UUID] = None
    animalId: Optional[UUID] = None
    price: Optional[float] = None




class Good(GoodBase):
    id: UUID

    class Config:
        from_attributes = True
        alias_generator = lambda name: name.lower()

class CartItemUpdate(BaseModel):
    cart_id: UUID
    good_id: UUID

class Cart(BaseModel):
    id: UUID  
    userId: UUID  
    goods: List[UUID] = []  

    class Config:
        from_attributes = True
        alias_generator = lambda name: name.lower()

class Category(BaseModel):
    id: UUID  
    title: str  

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    title: str  

    class Config:
        from_attributes = True

class Role(BaseModel):
    id: UUID  
    name: str  

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str  

    class Config:
        from_attributes = True

class Coupon(BaseModel):
    id: UUID  
    sale: int  

    class Config:
        from_attributes = True

class CouponCreate(BaseModel):
    sale: int  

    class Config:
        from_attributes = True

class Firm(BaseModel):
    id: UUID  
    naming: str  

    class Config:
        from_attributes = True

class FirmCreate(BaseModel):
    naming: str  

    class Config:
        from_attributes = True  


class Animal(BaseModel):
    id: UUID = Field(..., alias="id")
    type: str = Field(..., alias="type")



class AnimalCreate(BaseModel):
    type: str

class UserCreate(BaseModel):
    login: str
    password: str
    name: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    Login: Optional[str] = Field(None, max_length=64)  
    Password: Optional[str] = Field(None, max_length=64)  
    Name: Optional[str] = Field(None, max_length=64)  

    class Config:
        from_attributes = True  

class UserProfile(BaseModel):
    id: UUID
    login: str
    name: str
    roleId: UUID  
    couponId: Optional[UUID] = None
    banned: bool

    class Config:
        from_attributes = True
        alias_generator = lambda s: s.lower()

class User(BaseModel):
    id: UUID
    name: str
    banned: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str



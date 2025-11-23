from http.client import responses

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional
from typing import List
from .models import  AuctionStatus, FueltypeChoices, TransmissionChoices, \
    RoleChoices


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleChoices
    phone_number: Optional[str]


    class Config:
        from_attributes = True



class UserUpdateSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password:str
    role: RoleChoices
    phone_number: Optional[str]

    class Config:
        from_attributes = True


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    role: RoleChoices
    phone_number: Optional[str]


    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class CarCreateSchema(BaseModel):
    brand: str
    model: str
    year: date
    fuel_type: FueltypeChoices
    mileage: int
    transmissions: TransmissionChoices
    price: int
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class CarUpdateSchema(BaseModel):
    brand: str
    model: str
    year: date
    fuel_type: FueltypeChoices
    milage: int
    transmission: TransmissionChoices
    price: int
    description: str
    images: str

    class Config:
        from_attributes = True


class CarOutSchema(BaseModel):
    id: int
    brand: str
    model: str
    year: date
    fuel_type: FueltypeChoices
    mileage: int
    price: int
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class AuctionCreateSchema(BaseModel):
    car_id: int
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: AuctionStatus

    class Config:
        from_attributes = True


class AuctionUpdateSchema(BaseModel):
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: AuctionStatus

    class Config:
        from_attributes = True


class AuctionOutSchema(BaseModel):
    id: int
    car_id: int
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: AuctionStatus

    class Config:
        from_attributes = True


class BidSchema(BaseModel):
    auction_id: int
    user_id: int
    amount: int
    created_date: datetime

    class Config:
        from_attributes = True


class FeedbackSchema(BaseModel):
    seller_id: int
    buyer_id: int
    rating: int = Field(..., gt=1, lt=5)
    created_date: datetime

    class Config:
        from_attributes = True


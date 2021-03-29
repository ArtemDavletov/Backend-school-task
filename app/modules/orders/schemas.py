from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field, validator

from repository import couriers_repo
from settings.database import get_db


class OrderItem(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: List[str]

    @validator('weight')
    def validate_weight(cls, v):
        if v < 0.01 or v > 50:
            raise ValueError('Bad weigth')
        return v


class Order(BaseModel):
    id: int


class OrdersIds(BaseModel):
    orders: List[Order]


class OrderAP(BaseModel):
    class Config:
        extra = Extra.allow

    id: int


class OrdersIdsAP(BaseModel):
    class Config:
        extra = Extra.allow

    orders: List[OrderAP]


class AssignTime(BaseModel):
    assign_time: Optional[str] = Field(None, example='2021-01-10T09:32:14.42Z')


class OrdersAssignPostRequest(BaseModel):
    courier_id: int

    @validator('courier_id')
    def validate_weight(cls, v):
        courier_db = couriers_repo.get_courier_db(get_db(), v)
        if courier_db is None:
            raise ValueError('No such courier')
        return v


class OrdersCompletePostRequest(BaseModel):
    courier_id: int
    order_id: int
    complete_time: str = Field(..., example='2021-01-10T10:33:01.42Z')


class OrdersCompletePostResponse(BaseModel):
    order_id: int


class OrdersPostRequest(BaseModel):
    data: List[OrderItem]

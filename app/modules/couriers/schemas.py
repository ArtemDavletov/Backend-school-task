from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra


class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class CourierItem(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]


class Courier(BaseModel):
    id: int


class CouriersIds(BaseModel):
    couriers: List[Courier]


class Courier1(BaseModel):
    class Config:
        extra = Extra.allow

    id: int


class CouriersIdsAP(BaseModel):
    class Config:
        extra = Extra.allow

    couriers: List[Courier1]


class CourierGetResponse(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]
    rating: Optional[float] = None
    earnings: int


class CourierUpdateRequest(BaseModel):
    courier_type: Optional[CourierType] = None
    regions: Optional[List[int]] = None
    working_hours: Optional[List[str]] = None

    def to_dict(self):
        courier_dict = self.dict()

        if self.courier_type:
            courier_dict['courier_type'] = self.courier_type.value
        return courier_dict


class CouriersPostRequest(BaseModel):
    data: List[CourierItem]

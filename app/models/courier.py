from sqlalchemy import Column, Integer, String, Float, PickleType
from sqlalchemy.orm import relationship

from app.modules.couriers.schemas import CourierGetResponse, CourierItem, CourierType
from app.settings.database import Base


class CourierDB(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, unique=True, index=True, primary_key=True)
    courier_type = Column(String)
    regions = Column(PickleType)
    working_hours = Column(PickleType)
    rating = Column(Float)
    earnings = Column(Integer, default=0)

    orders = relationship('OrderDB', back_populates='courier')

    def to_courier_schema(self) -> CourierGetResponse:
        return CourierGetResponse(courier_id=self.id,
                                  courier_type=CourierType(self.courier_type),
                                  regions=self.regions,
                                  working_hours=self.working_hours,
                                  rating=self.rating,
                                  earnings=self.earnings)

    def to_courier_item_schema(self) -> CourierItem:
        return CourierItem(courier_id=self.id,
                           courier_type=CourierType(self.courier_type),
                           regions=self.regions,
                           working_hours=self.working_hours)

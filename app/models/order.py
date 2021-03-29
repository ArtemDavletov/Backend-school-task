import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

from app.settings.database import Base


class OrderDB(Base):
    __tablename__ = 'orders'

    id = Column(Integer, unique=True, index=True, primary_key=True)
    weight = Column(Float)
    region = Column(Integer)
    delivery_hours = ARRAY(String)
    assign_time = Column(DateTime, default=datetime.datetime.utcnow)
    complete_time = Column(DateTime)
    courier_id = Column(Integer, ForeignKey('couriers.id'), default=None)

    courier = relationship('CourierDB')

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.models.courier import CourierDB
from app.models.order import OrderDB
from app.settings.database import get_db

router = APIRouter()

__all__ = (
    'router',
)


@router.get('/o')
async def order(
        db: Session = Depends(get_db)
):
    return db.query(OrderDB).all()


@router.get('/c')
async def couriers(
        db: Session = Depends(get_db)
):
    return db.query(CourierDB).all()


@router.get('/health')
async def health():
    return Response(content='success')

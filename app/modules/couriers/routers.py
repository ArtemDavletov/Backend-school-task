import logging

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from starlette import status

from app.models.courier import CourierDB
from app.modules.couriers.schemas import CouriersPostRequest, CouriersIds, Courier, CourierItem, CourierUpdateRequest
from app.repository import couriers_repo
from app.settings.database import get_db

router = APIRouter()

__all__ = (
    'router',
)


@router.post(
    '/',
    description='Import couriers',
    responses={
        "201": {
            "description": "Created",
        },
        "400": {
            "description": "Bad request",
        }
    }
)
def import_couriers(
        couriers_post_request: CouriersPostRequest,
        db: Session = Depends(get_db)
):
    couriers = []
    try:
        for courier in couriers_post_request.data:
            couriers.append(Courier(id=couriers_repo.create_courier(db, courier).id))
        return CouriersIds(couriers=couriers)
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/{courier_id}',
    description='Get couriers info',
    responses={
        "200": {
            "description": "OK",
        },
        "404": {
            "description": "Not found"
        }
    }
)
def get_courier(
        courier_id: int,
        db: Session = Depends(get_db)
):
    try:
        courier: CourierDB = couriers_repo.get_courier_db(db, courier_id)

        if courier is None:
            logging.info(f"No such courier with id: {courier_id}")
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return courier.to_courier_schema()
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch(
    '/{courier_id}',
    description='Update couriers by id',
    responses={
        "200": {
            "description": "Created",
        },
        "400": {
            "description": "Bad request"
        },
        "404": {
            "description": "Not found"
        }
    }
)
def update_courier(
        courier_id: int,
        values: CourierUpdateRequest,
        db: Session = Depends(get_db)
):
    try:
        courier: CourierDB = couriers_repo.update_courier(db, courier_id, values)

        if courier is None:
            logging.info(f"No such courier with id: {courier_id}")
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return courier.to_courier_item_schema()
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

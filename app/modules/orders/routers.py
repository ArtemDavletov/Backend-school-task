import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from modules.orders.schemas import OrdersPostRequest, Order, OrdersIds, OrdersAssignPostRequest, \
    OrdersCompletePostRequest, OrdersCompletePostResponse
from repository import orders_repo
from settings.database import get_db

router = APIRouter()

__all__ = (
    'router',
)


@router.post(
    '/',
    description='Import orders',
    responses={
        "201": {
            "description": "Created",
        },
        "400": {
            "description": "Bad request",
        }
    }
)
async def import_orders(
        order_item: OrdersPostRequest,
        db: Session = Depends(get_db)
):
    orders = []
    try:
        for order in order_item.data:
            orders.append(Order(id=orders_repo.create_order(db, order).id))
        return Response(status_code=status.HTTP_201_CREATED, content=OrdersIds(orders=orders).json())  # CouriersIds
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)  # CouriersIdsAP


@router.post(
    '/assign',
    description='Assign orders to a couriers by id',
    responses={
        "200": {
            "description": "OK",
        },
        "400": {
            "description": "Bad request",
        }
    }
)
async def orders_assign(
        order_assign: OrdersAssignPostRequest,
        db: Session = Depends(get_db)
):
    try:
        return OrdersIds(orders=list(map(lambda x: Order(id=x.id), orders_repo.assign_order(db, order_assign))))
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    '/complete',
    description='Marks orders as completed',
    responses={
        "200": {
            "description": "Ok",
        },
        "400": {
            "description": "Bad request",
        }
    }
)
async def orders_complete(
        order_complete: OrdersCompletePostRequest,
        db: Session = Depends(get_db)
) -> OrdersCompletePostResponse:
    try:
        return OrdersCompletePostResponse(order_id=orders_repo.complete_order(db, order_complete))
    except Exception as e:
        logging.error(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

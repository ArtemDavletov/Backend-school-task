from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.order import OrderDB
from modules.orders.schemas import OrderItem, OrdersAssignPostRequest, OrdersCompletePostRequest


def create_order(
        db: Session,
        order: OrderItem
) -> OrderDB:
    db_order = OrderDB(id=order.order_id,
                       weight=order.weight,
                       region=order.region,
                       delivery_hours=order.delivery_hours)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def assign_order(
        db: Session,
        order_assign: OrdersAssignPostRequest
) -> List[OrderDB]:
    # courier: CourierDB = couriers_repo.get_courier_db(db, order_assign.courier_id)
    order_db: OrderDB = db.query(OrderDB).filter_by(courier=None).order_by(desc(OrderDB.assign_time)).first()
    order_db.courier_id = order_assign.courier_id
    # db.refresh(order_db)
    db.add(order_db)
    db.commit()

    return [order_db]


def complete_order(
        db: Session,
        order: OrdersCompletePostRequest
) -> int:
    order_db = db.query(OrderDB) \
        .filter(OrderDB.id == order.order_id and
                OrderDB.courier == order.courier_id).first()

    order_db.complete_time = order.complete_time
    db.add(order_db)
    db.commit()

    return order.order_id

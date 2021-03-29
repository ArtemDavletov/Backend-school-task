from sqlalchemy.orm import Session

from models.courier import CourierDB
from modules.couriers.schemas import CourierItem, CourierUpdateRequest


def create_courier(
        db: Session,
        courier_item: CourierItem
) -> CourierDB:
    db_courier = CourierDB(id=courier_item.courier_id,
                           courier_type=courier_item.courier_type.value,
                           regions=courier_item.regions,
                           working_hours=courier_item.working_hours)

    db.add(db_courier)
    db.commit()

    return db_courier


def get_courier_db(
        db: Session,
        courier_id: int
) -> CourierDB:
    return db.query(CourierDB).filter(CourierDB.id == courier_id).first()


def update_courier(
        db: Session,
        courier_id: int,
        values: CourierUpdateRequest
) -> CourierDB:
    db.query(CourierDB).filter(CourierDB.id == courier_id).update(values.to_dict())
    db.commit()
    courier = get_courier_db(db, courier_id)
    return courier

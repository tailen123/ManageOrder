from sqlalchemy.orm import Session
from ManageOrder.models import models_order
from ManageOrder.database.databases_order import atomicity


# @atomicity
# 获取多个订单
def get_orders_from_db(db: Session, skip: int = 0, limit: int = 100):
    orders = db.query(models_order.Order).filter(models_order.Order.flag_id == 1).offset(skip).limit(limit).all()
    return orders


# 创建订单
def create_order(db: Session, order_id: int, note: str):
    db_order = models_order.Order(note=note, order_id=order_id, flag_id=1)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# 查询订单
def get_order_by_id(db: Session, order_id: int):
    db_order = db.query(models_order.Order).filter(models_order.Order.order_id == order_id, models_order.Order.flag_id == 1).first()
    # if db_order.flag_id:
    return db_order
    # return {"message": "订单已删除"}


# 删除订单

def delete_order(db: Session, order_id: int):
    db_order = db.query(models_order.Order).filter(models_order.Order.order_id == order_id).first()
    db_order.flag_id = 0
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# 修改订单

def update_order(db: Session, order_id: int, new_note: str):
    db_order = db.query(models_order.Order).filter(models_order.Order.order_id == order_id).first()
    db_order.note = new_note
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

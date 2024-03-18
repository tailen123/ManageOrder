# routes.py

from fastapi import APIRouter, Depends, FastAPI

from ManageOrder.crud.crud_order import get_orders_from_db, get_order_by_id, delete_order, update_order, create_order
from sqlalchemy.orm import Session
from ManageOrder.database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request
import jwt
from pydantic import BaseModel
from ManageOrder.schemas.schemas_order import Order, Order_list
from ManageOrder.middleware.middleware import auth_check

app = FastAPI()
router = APIRouter(dependencies=[Depends(auth_check)])

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"


# async def middleware(request: Request, call_next):
#     try:
#         token: str = request.headers["Authorization"].split()[1]
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#
#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         request.state.user = username
#     except(KeyError, IndexError, jwt.PyJWTError):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
#     response = await call_next(request)
#     return response


@router.get("/")
async def get_orders(db: Session = Depends(get_db)):
    orders =get_orders_from_db(db)
    return orders


@router.get("/orders/{order_id}")
async def get_one_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id=order_id)


@router.post("/orders/", response_model=Order)
async def create_new_item(order_id: int, note: str, db: Session = Depends(get_db)):
    return create_order(db, order_id=order_id, note=note)


@router.patch("/orders/{order_id}")
async def update_note(order_id: int, new_note: str, db: Session = Depends(get_db)):
    return update_order(db, order_id=order_id, new_note=new_note)


@router.delete("/orders/{order_id}")
async def delete_order( order_id: int,db: Session=Depends(get_db)):
    return delete_order(db, order_id)

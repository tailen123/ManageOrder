# routes.py

from fastapi import APIRouter, Depends, FastAPI
from ManageOrder.models.models_order import Order
from ManageOrder.crud.crud_order import get_orders, get_order_by_id, delete_order, update_order, create_order
from sqlalchemy.orm import Session
from ManageOrder.database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request
import jwt


app = FastAPI()
router = APIRouter()

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"


async def middleware(request: Request, call_next):
    try:
        token: str = request.headers["Authorization"].split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.user = username
    except(KeyError, IndexError, jwt.PyJWTError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    response = await call_next(request)
    return response


@router.get("/")
async def get_orders(db: Session = Depends(get_db)):
    orders = get_orders(db)
    return orders


@router.get("/orders/{order_id}")
async def get_one_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id=order_id)


@router.post("/orders/")
async def create_new_item(order_id: int, note: str, db: Session = Depends(get_db), ):
    return create_order(db, order_id=order_id, note=note)


@router.patch("/orders/{order_id}")
async def update_note(db: Session, order_id: int, new_note: str):
    return update_order(db, order_id=order_id, new_note=new_note)


@router.delete("/orders/{order_id}")
async def delete_order(db: Session, order_id: int):
    return delete_order(db, order_id)


app.include_router(router, prefix="/order/", tags=["order"])
app.middleware(middleware)

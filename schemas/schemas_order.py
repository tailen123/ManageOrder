from pydantic import BaseModel


class OrderBase(BaseModel):
    order_id: int
    note: str


class OrderCreate(OrderBase):
    flag_id: int


class Order(OrderBase):
    order_id: int

    class Config:
        from_attributes = True


class Order_list(BaseModel):
    orders: list[Order]

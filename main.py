from fastapi import FastAPI
from ManageOrder.router.router_order import router as router_order
from ManageOrder.router.router_login import router as router_log

app = FastAPI()

# 添加订单相关路由分组
app.include_router(router_order, prefix="/orders", tags=["orders"])
app.include_router(router_log, prefix="/login", tags=["login"])

# 添加用户相关路由分组


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

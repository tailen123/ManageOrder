from fastapi import FastAPI
from ManageOrder.router.router_order import router as router_order
from ManageOrder.router.router_login import router as router_log
from ManageOrder.middleware.middleware import middleware

app = FastAPI()
app.middleware("http")(middleware)
# 添加订单相关路由分组
app.include_router(router_order, prefix="/orders/", tags=["orders"])
app.include_router(router_log,prefix="/",tags=["login"])

# 添加用户相关路由分组


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

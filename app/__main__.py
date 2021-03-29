import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

from settings.database import Base, engine
from settings.settings import settings

from modules.default.routers import router as default_router
from modules.couriers.routers import router as couriers_router
from modules.orders.routers import router as orders_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


app.include_router(default_router, tags=['default'])
app.include_router(couriers_router, tags=['couriers'], prefix='/couriers')
app.include_router(orders_router, tags=['orders'], prefix='/orders')

if __name__ == '__main__':
    uvicorn.run(
        '__main__:app',
        host=settings.APP_HOST,
        reload=settings.DEBUG_MODE,
        port=settings.APP_PORT,
    )

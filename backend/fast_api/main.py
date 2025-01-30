import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from backend.fast_api.models import BaseResponse
from backend.fast_api.routers import web_app

app = FastAPI()


# === Глобальные обработчики исключений ===

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Глобальный обработчик для HTTPException, возвращающий ответ в стиле BaseResponse.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            status_code=exc.status_code,
            errors=[exc.detail],
            content=None
        ).model_dump()
    )


@app.exception_handler(Exception)
async def custom_generic_exception_handler(request: Request, exc: Exception):
    """
    Глобальный обработчик для всех прочих исключений.
    """
    return JSONResponse(
        status_code=500,
        content=BaseResponse(
            status_code=500,
            errors=["An internal server error occurred."],
            content=None
        ).model_dump()
    )


# === Подключение маршрутов ===

app.include_router(web_app.router, prefix="/api/v1", tags=["WebApp"])

if __name__ == '__main__':
    uvicorn.run(app,
                port=8000)

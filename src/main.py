from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from typing import cast
from time import time

from src.routers.auth_router import AuthRouter
from src.routers.product_router import ProductRouter
from src.exceptions.exceptions import DefaultException
from src.exceptions.no_content import NoContentException, ExceptionsEnum
from src.models.response_dto import Content, MetaContent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(AuthRouter().router)
app.include_router(ProductRouter().router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(Exception)
async def exception_handler(req: Request, exc: Exception):
    if isinstance(exc, DefaultException):
        if isinstance(exc, NoContentException):
            return Response(status_code=ExceptionsEnum.NoContent.value) 
        exc = cast(DefaultException, exc)
        return JSONResponse(
            status_code=exc.code.value,
            content=Content(data=None, meta=MetaContent(
                    code=exc.code.value,
                    message=exc.message
                )).model_dump()
            )
    return exc

@app.exception_handler(RequestValidationError)
async def exception_handler(req: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=Content(data=exc._errors, meta=MetaContent(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message='',
            )).model_dump()
        )
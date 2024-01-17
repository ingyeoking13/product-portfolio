from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import cast

from src.routers.auth_router import AuthRouter
from src.exceptions.exceptions import DefaultException
from src.models.response import Content, MetaContent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(AuthRouter().router)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    if isinstance(exc, DefaultException):
        exc = cast(DefaultException, exc)
        return JSONResponse(
            status_code=exc.code.value,
            content=Content(data=None, meta=MetaContent(
                    code=exc.code.value,
                    message=exc.message
                )).model_dump()
            )
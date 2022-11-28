# project/app/main.py

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api import ping, summaries  # updated
from app.db import init_db
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"]
    )  # new
    return application


app = create_application()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()
    modified_details = []
    # Replace 'msg' with 'message' for each error
    for error in details:
        msg ='asegúrese de que este valor sea mayor que 0' if error["msg"] =='ensure this value is greater than 0' else error["msg"]
        modified_details.append(
            {
                "loc": error["loc"],
                "msg": msg,
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )

@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")

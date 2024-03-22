from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import importData
import json
import logging
import sys
from .. import database as db
import sqlalchemy

description = """
___
"""

app = FastAPI(
    title="FANTASY PREMIER LEAGUE STATS",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Pau Minguet",
        "email": "pminguet@calpoly.edu",
    },
)



app.include_router(importData.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    with db.engine.begin() as connection:
        row = connection.execute(sqlalchemy.text("SELECT * FROM users")).first()
        print(row[2])
    return row[2]
from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
#from src.api import audit, carts, catalog, bottler, barrels, admin
from src.api import users, groups
import json
import logging
import sys
from .. import database as db
import sqlalchemy

description = """
Bettermo is the place to go for group purchases
"""

app = FastAPI(
    title="Bettermo",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Nick Hotelling",
        "email": "nhotelli@calpoly.edu",
    },
)




#app.include_router(audit.router)
app.include_router(users.router)
app.include_router(groups.router)

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
    return {"message": "Welcome to the better version of Venmo"}
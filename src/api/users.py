from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter

router = APIRouter(
    prefix="/user",
    tags=["user"],
    #dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    name: str
    email: str
    phone: str

@router.post("/create")
def post_deliver_bottles(newuser: User):

    with db.engine.begin() as connection:
        id = connection.execute(sqlalchemy.text("INSERT INTO users (name, email, phone) VALUES ("+newuser.name+", "+newuser.email+", "+newuser.phone+") RETURNING id")).scalar_one()
   
    return {'new_user_id': id}


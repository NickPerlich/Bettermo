from fastapi import APIRouter, Depends
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
        id = connection.execute(sqlalchemy.text("""INSERT INTO users (name, email, phone) 
                                                VALUES (:name, :email, :phone) RETURNING id"""), {
                                                    'name': newuser.name,
                                                    'email': newuser.email,
                                                    'phone': newuser.phone
                                                }).scalar_one()
   
    return {'new_user_id': id}


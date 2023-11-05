from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    name: str
    email: str
    phone: str

@router.post("/")
def post_deliver_bottles(newuser: User):

    with db.engine.begin() as connection:
        id = connection.execute(sqlalchemy.text("""INSERT INTO users (name, email, phone) 
                                                VALUES (:name, :email, :phone) RETURNING id"""), {
                                                    'name': newuser.name,
                                                    'email': newuser.email,
                                                    'phone': newuser.phone
                                                }).scalar_one()
   
    return {'new_user_id': id}

@router.get("/{user_id}/balances/{other_user_id}")
def get_user_balance(user_id: int, other_user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                '''
                WITH outbound as (
                    SELECT COALESCE(SUM(value), 0) amount
                    FROM transactions
                    WHERE from_user = :uid1 AND to_user = :uid2
                ),
                inbound as (
                    SELECT COALESCE(SUM(value), 0) amount
                    FROM transactions
                    WHERE to_user = :uid1 AND from_user = :uid2
                )
                SELECT (inbound.amount - outbound.amount) as amount
                FROM inbound CROSS JOIN outbound
                '''
            ),
            {
                'uid1': user_id,
                'uid2': other_user_id
            }
        ).scalar_one()
    return {"Balance": result}



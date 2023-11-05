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

class Payment(BaseModel):
    amount: float
    description: str

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

@router.post("/{uid1}/pay/{uid2}")
def post_payment(uid1: int, uid2: int, payment: Payment):

    with db.engine.begin() as connection:
        id = connection.execute(sqlalchemy.text("""INSERT INTO transactions (from_user, to_user, value)
                                                    VALUES (:user1, :user2, ROUND(:payment, 2))"""), {
                                                    'user1': uid1,
                                                    'user2': uid2,
                                                    'payment': payment.amount
                                                }).scalar_one()
        connection.execute(sqlalchemy.text("""INSERT INTO settlements (description, transaction_id)
                                                VALUES (:desc, :tid)"""), {
                                                    'desc': payment.description,
                                                    'tid': id
                                                })
        
    return str(payment.amount)


from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError

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

@router.post("/create_user")
def create_user(new_user: User):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO users (name, email, phone) 
                                                    VALUES (:name, :email, :phone) RETURNING id"""), {
                                                        'name': new_user.name,
                                                        'email': new_user.email,
                                                        'phone': new_user.phone
                                                    }).scalar_one()
    
        return {'new_user_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.get("/{user_id}/balances/{other_user_id}")
def get_user_balance(user_id: int, other_user_id: int):
    try:
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
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.post("/{user_id}/pay/{other_user_id}")
def post_payment(user_id: int, other_user_id: int, payment: Payment):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO transactions (from_user, to_user, value)
                                                        VALUES (:user1, :user2, ROUND(:payment, 2))
                                                        RETURNING id
                                                    """), {
                                                        'user1': user_id,
                                                        'user2': other_user_id,
                                                        'payment': payment.amount
                                                    }).scalar_one()
            connection.execute(sqlalchemy.text("""INSERT INTO settlements (description, transaction_id)
                                                    VALUES (:desc, :tid)"""), {
                                                        'desc': payment.description,
                                                        'tid': id
                                                    })
            
        return {"Amount paid": payment.amount}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.get("/{user_id}/balance_breakdown")
def get_balance_breakdown(user_id: int):
    try:
        with db.engine.begin() as connection:
            result = connection.execute(
                sqlalchemy.text(
                    '''
                    WITH outbound AS (
                    SELECT SUM(value) AS amount, to_user AS user_id
                    FROM transactions
                    WHERE from_user = 101
                    GROUP BY to_user
                    ),
                    inbound AS (
                        SELECT SUM(value) AS amount, from_user AS user_id
                        FROM transactions
                        WHERE to_user = 101
                        GROUP BY from_user
                    )
                    SELECT user_id, amount
                    FROM outbound
                    WHERE amount > 0

                    UNION

                    SELECT user_id, -amount AS amount
                    FROM inbound
                    WHERE amount < 0
                    '''
                ),
                {
                    'uid1': user_id
                }
            ).fetchall()
        return {"Balance Breakdown": result}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.post("/{user_id}/resolve_balance")
def post_resolve_balance(user_id: int):
    try:
        with db.engine.begin() as connection:
            result = connection.execute(
                sqlalchemy.text(
                    '''
                    SELECT to_user AS user, SUM(value) AS amount
                    FROM transactions
                    WHERE from_user = 101
                    GROUP BY user
                    '''
                ),
                {
                    'uid1': user_id
                }
            ).fetchall()

            for i in result:
                id = connection.execute(sqlalchemy.text("""INSERT INTO transactions (from_user, to_user, value)
                                                        VALUES (:user1, :user2, ROUND(:payment, 2))
                                                        RETURNING id
                                                    """), {
                                                        'user1': user_id,
                                                        'user2': i[0],
                                                        'payment': i[1]
                                                    }).scalar_one()

        return {"All balances settled"}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

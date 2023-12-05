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


@router.put("/{user_id}/update_user")
def update_user_info(user_id: int, new_user: User):
    try:
        with db.engine.begin() as connection:
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE users 
                    SET name = :name, email = :email, phone = :phone
                    where id = :id
                    """
                ),
                    {
                        'id': user_id,
                        'name': new_user.name,
                        'email': new_user.email,
                        'phone': new_user.phone
                    }
                
            )
        return "OK"
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

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
                    with outbound as (
                        SELECT to_user, COALESCE(SUM(value), 0) amount
                        FROM transactions
                        WHERE from_user = :uid1
                        group by to_user
                    ),
                    inbound as (
                        SELECT from_user, COALESCE(SUM(value), 0) amount
                        FROM transactions
                        WHERE to_user = :uid1
                        group by from_user
                    )
                    SELECT inbound.from_user as user, (inbound.amount - outbound.amount) as amount
                    FROM inbound 
                    join outbound on inbound.from_user = outbound.to_user
                    '''
                ),
                {
                    'uid1': user_id
                }
            ).fetchall()
            
            #Put returned values into json format
            result_dict = {}
            for item in result:
                result_dict[item[0]] = item[1]
            
        return {"Balance Breakdown": result_dict}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")


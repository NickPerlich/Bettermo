from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    #dependencies=[Depends(auth.get_api_key)],
)

class Group(BaseModel):
    name: str
    description: str

@router.put("/{group_id}/update_group")
def update_group_info(group_id: int, new_group:Group):
    try:
        with db.engine.begin() as connection:
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE groups
                    SET name = :name, description = :description
                    where id = :gid
                    """
                ),
                {
                    'gid': group_id,
                    'name': new_group.name,
                    'description': new_group.description
                }
            )
        return "OK"
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")


@router.post("/create_group")
def create_group(new_group: Group):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(
                sqlalchemy.text('''INSERT INTO groups (name, description)
                                VALUES (:g_name, :descript) RETURNING id'''),
                {
                    'g_name': new_group.name,
                    'descript': new_group.description
                }
            ).scalar_one()
    
        return {'new_group_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.get("/{group_id}")
def get_group(group_id: int):
    try:
        with db.engine.begin() as connection:
            result = connection.execute(
                sqlalchemy.text('''select user_id, name, email, phone
                                from users_to_group
                                join users on user_id = users.id
                                where group_id = :gid
                                order by user_id'''), {
                                    'gid': group_id
                                }
            ).all()
        users = []
        for row in result:
            users.append({
                'user_id': row.user_id,
                'name': row.name,
                'email': row.email,
                'phone': row.phone
            })
        return users
    
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.delete("/{group_id}/users/{user_id}")
def delete_user_from_group(group_id: int, user_id: int):
    try:
        with db.engine.begin() as connection:
            result = connection.execute(
                sqlalchemy.text('''select user_id, name, email, phone
                                from users_to_group
                                join users on user_id = users.id
                                where group_id = :gid and user_id = :uid
                                order by user_id'''), {
                                    'gid': group_id,
                                    'uid': user_id
                                })
            connection.execute(
                sqlalchemy.text('''delete
                                from users_to_group
                                where group_id = :gid and user_id = :uid'''), {
                                    'gid': group_id,
                                    'uid': user_id
                                }
            )

            result = result.first()
            print(result[0])
            return {
                'deleted_user_id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3]
            }
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

@router.post("/{group_id}/users/{user_id}")
def post_add_user_to_group(group_id: int, user_id: int):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(
                sqlalchemy.text('''INSERT INTO users_to_group (user_id, group_id)
                                VALUES (:uid, :gid) RETURNING id'''),
                {
                    'uid': user_id,
                    'gid': group_id 
                }
            ).scalar_one()
    
        return {'id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

class PurchaseInfo(BaseModel):
    description: str
    price: float

@router.post("/{group_id}/users/{user_id}/purchases")
def post_group_purchase(group_id: int, user_id: int, purchase: PurchaseInfo):
    try:
        with db.engine.begin() as connection:
            #create purchase
            purchase_id = connection.execute(
                sqlalchemy.text('''INSERT into purchases (group_id, buyer, description, price)
                                VALUES (:gid, :uid, :description, :price)
                                RETURNING id'''),
                {
                    'gid': group_id,
                    'uid': user_id,
                    'description': purchase.description,
                    'price': purchase.price
                }
            ).scalar_one()

            #create transactions
            transaction_ids = connection.execute(
                sqlalchemy.text(
                    '''
                    WITH groupmates as (
                        SELECT DISTINCT user_id
                        FROM users_to_group
                        WHERE group_id = :gid AND NOT user_id = :uid
                    ),
                    total_groupmates as (
                        SELECT COUNT(*) as total
                        FROM groupmates
                    )
                    INSERT INTO transactions
                    (from_user, to_user, value)
                    SELECT :uid, groupmates.user_id, ROUND(:price / (total_groupmates.total+1),2)
                    FROM groupmates CROSS JOIN total_groupmates
                    RETURNING id
                    '''
                ),
                {
                    'gid': group_id,
                    'uid': user_id,
                    'price': purchase.price
                }
            ).all()

            transaction_ids = [id.id for id in transaction_ids]

            #create purchase_transactions
            for id in transaction_ids:
                connection.execute(
                    sqlalchemy.text(
                        '''
                        INSERT INTO purchase_transactions
                        (purchase_id, transaction_id)
                        VALUES
                        (:pid, :tid)
                        '''
                    ),
                    {
                        'pid': purchase_id,
                        'tid': id
                    }
                )
        return "OK"
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")
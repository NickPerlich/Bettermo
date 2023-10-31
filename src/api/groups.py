from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    #dependencies=[Depends(auth.get_api_key)],
)

class Group(BaseModel):
    name: str
    description: str

@router.post("/")
def post_deliver_bottles(newgroup: Group):

    with db.engine.begin() as connection:
        id = connection.execute(
            sqlalchemy.text('''INSERT INTO groups (name, description)
                            VALUES (:g_name, :descript) RETURNING id'''),
            {
                'g_name': newgroup.name,
                'descript': newgroup.description
            }
        ).scalar_one()
   
    return {'new_group_id': id}
@router.post("/{group_id}/addUser/{user_id}")
def post_deliver_bottles(group_id: int, user_id: int):

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

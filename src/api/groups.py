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
    dscription: str

@router.post("/create")
def post_deliver_bottles(newgroup: Group):

    with db.engine.begin() as connection:
        id = connection.execute(sqlalchemy.text("INSERT INTO groups (name, description) VALUES ("+newgroup.name+", "+newgroup.description+") RETURNING id")).scalar_one()
   
    return {'new_group_id': id}

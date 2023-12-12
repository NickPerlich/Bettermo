from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError

router = APIRouter(
    prefix="/calculate",
    tags=["calculate"],
    #dependencies=[Depends(auth.get_api_key)],
)

class OneRepMax(BaseModel):
    weight: float
    reps: int


@router.post("/onerm")
def create_user(OneRepMax: OneRepMax):
    try:
        result = round(OneRepMax.weight*(1+(OneRepMax.reps/30)),2)
        return {'One Rep Max': result}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError

router = APIRouter(
    prefix="/log",
    tags=["log"],
    #dependencies=[Depends(auth.get_api_key)],
)

class Weight(BaseModel):
    user_id: int
    exercise_id: int
    weight: float
    reps: int

@router.post("/exercise")
def log_exercise(new_weight: Weight):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO logs (user_id, exercise_id, weight, reps, onerm) 
                                                    VALUES (:user_id, :exercise_id, :weight, :reps, :onerm) RETURNING id"""), {
                                                        'user_id': new_weight.user_id,
                                                        'exercise_id': new_weight.exercise_id,
                                                        'weight': new_weight.weight,
                                                        'reps': new_weight.reps,
                                                        'onerm': round(new_weight.weight*(1+(new_weight.reps/30)),2)
                                                    }).scalar_one()
    
        return {'new_weight_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")
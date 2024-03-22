import math
from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
import requests
import sys
from unidecode import unidecode
import getTeams

router = APIRouter(
    prefix="/importData",
    tags=["importData"],
    #dependencies=[Depends(auth.get_api_key)],
)



@router.get("/update-teams")
def update_times():
    teams = getTeams.fetch_team_data()

    print(teams)

    try:
        with db.engine.begin() as connection:
            workout_times = connection.execute(sqlalchemy.text("""  select w.id, sum(ws.sets * :time_for_set + (ws.sets-1) * ws.rest_secs), count(*)
                                                            from splits s 
                                                            join workouts w on w.split_id = s.id
                                                            join workout_steps ws on ws.workout_id = w.id
                                                            where s.id = :split_id
                                                            group by w.id
                                                        """), {'time_for_set': time_for_set,
                                                                'split_id': split_id
                                                                }).fetchall()
     
    
        return "Ok"
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")




@router.get("/players")
def get_split(split_id):
    try:
        split = {}

        with db.engine.begin() as connection:
            s = connection.execute(sqlalchemy.text("""
                                                       SELECT s.id, s.created_at, s.name, s.description, i.username, s.difficulty, o.name, floor(s.avg_duration/60)
                                                       from splits s 
                                                       join influencers i on i.id = s.author_id
                                                       join objectives o on o.id = s.objective_id
                                                       where s.id = :id
                                                       """), {'id': split_id}).fetchone()
            split['id'] = s[0]
            split['created_at'] = s[1]
            split['name'] = s[2]
            split['description'] = s[3]
            split['author'] = s[4]
            split['difficulty'] = s[5]
            split['objective'] = s[6]
            split['avg_duration'] = s[7]
            split['workouts'] = []

            w = connection.execute(sqlalchemy.text("""
                                                       SELECT id, name, day_of_week, duration
                                                       from workouts
                                                       where split_id = :id
                                                       """), {'id': s[0]}).fetchall()
            print(w)
            for i in w:
                workout = {}
                workout['name'] = i[1]
                workout['day_of_week'] = i[2]
                workout['duration'] = i[3]
                ex = connection.execute(sqlalchemy.text("""
                                                       SELECT e.name, w.max, w.sets, w.reps, w.percent_max_weight, w.rest_secs
                                                       from workout_steps w
                                                       join exercises e on e.id = w.exercise_id
                                                       where w.workout_id = :id
                                                       """), {'id': i[0]}).fetchall()
                dics = []
                for i in ex:
                    d = {}
                    d['name'] = i[0]
                    d['max'] = i[1]
                    d['sets'] = i[2]
                    d['reps'] = i[3]
                    d['percent_max_weight'] = i[4]
                    d['rest_secs'] = i[5]
                    dics.append(d)
                
                workout['steps'] = dics
                split['workouts'].append(workout)

            print(workout)
                
        
        
        

        
        return split
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")





@router.get("/update-times/{split_id}")
def update_times(split_id):

    time_for_set = 30
    time_between_exercises = 120

    try:
        with db.engine.begin() as connection:
            workout_times = connection.execute(sqlalchemy.text("""  select w.id, sum(ws.sets * :time_for_set + (ws.sets-1) * ws.rest_secs), count(*)
                                                            from splits s 
                                                            join workouts w on w.split_id = s.id
                                                            join workout_steps ws on ws.workout_id = w.id
                                                            where s.id = :split_id
                                                            group by w.id
                                                        """), {'time_for_set': time_for_set,
                                                                'split_id': split_id
                                                                }).fetchall()
            
            print(workout_times)

            for i in workout_times:
                id, duration = i[0], i[1] + time_between_exercises * (i[2]-1)
                connection.execute(sqlalchemy.text("""  update workouts
                                                        set duration = :duration
                                                        where id = :id
                                                        """), {'duration': duration,
                                                                'id': id
                                                                })
            
            connection.execute(sqlalchemy.text("""  UPDATE splits
                                                    SET avg_duration = (
                                                        SELECT a.dur
                                                        FROM (
                                                            SELECT AVG(w.duration) AS dur
                                                            FROM splits s 
                                                            JOIN workouts w ON w.split_id = s.id
                                                            WHERE s.id = :split_id
                                                        ) a
                                                    )
                                                    WHERE splits.id = :split_id
                                                        """), {'split_id': split_id
                                                                })
            

        return "Ok"
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")

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
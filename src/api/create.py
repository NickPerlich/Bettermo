from fastapi import APIRouter, Depends
from pydantic import BaseModel
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError

router = APIRouter(
    prefix="/create",
    tags=["create"],
    #dependencies=[Depends(auth.get_api_key)],
)




class User(BaseModel):
    username: str
    email: str


@router.post("/user")
def create_user(new_user: User):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO users (username, email) 
                                                    VALUES (:username, :email) RETURNING id"""), {
                                                        'username': new_user.username,
                                                        'email': new_user.email
                                                    }).scalar_one()
    
        return {'new_user_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")



class Influencer(BaseModel):
    username: str
    email: str


@router.post("/influencer")
def create_influencer(new_user: Influencer):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO influencers (username, email) 
                                                    VALUES (:username, :email) RETURNING id"""), {
                                                        'username': new_user.username,
                                                        'email': new_user.email
                                                    }).scalar_one()
    
        return {'new_influencer_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")
    

class Split(BaseModel):
    name: str
    description: str
    author_id: int
    difficulty: int
    objective_id: int

@router.post("/split")
def create_split(new_split: Split):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text(
                """INSERT INTO splits (name, description, author_id, difficulty, objective_id) 
                                                    VALUES (:name, :description, :author_id, :difficulty, :objective_id) RETURNING id"""), {
                                                        'name': new_split.name,
                                                        'description': new_split.description,
                                                        'difficulty': new_split.difficulty,
                                                        'author_id': new_split.author_id,
                                                        'objective_id': new_split.objective_id
                                                    }).scalar_one()
    
        return {'new_split_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")




class Workout(BaseModel):
    name: str
    split_id: int
    day_of_week: str


@router.post("/workout")
def create_workout(new_workout: Workout):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text(
                """INSERT INTO workouts (name, split_id, day_of_week) 
                   VALUES (:name, :split_id, :day_of_week) RETURNING id"""), {
                            'name': new_workout.name,
                            'split_id': new_workout.split_id,
                            'day_of_week': new_workout.day_of_week
                            }).scalar_one()
    
        return {'new_workout_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")



class Exercise(BaseModel):
    name: str
    equipment_id: int
    muscle_group: str


@router.post("/exercise")
def create_exercise(new_exercise: Exercise):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO exercises (name, equipment_id, muscle_group) 
                                                    VALUES (:name, :equipment_id, :muscle_group) RETURNING id"""), {
                                                        'name': new_exercise.name,
                                                        'equipment_id': new_exercise.equipment_id,
                                                        'muscle_group': new_exercise.muscle_group,
                                                    }).scalar_one()
    
        return {'new_exercise_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")



class WorkoutStep(BaseModel):
    workout_id: int
    exercise_id: int
    max: bool
    sets: int
    reps: int
    percent_max_weight: int
    rest_secs: int

@router.post("/step")
def create_step(new_step: WorkoutStep):
    try:
        with db.engine.begin() as connection:
            id = connection.execute(sqlalchemy.text("""INSERT INTO workout_steps (workout_id, exercise_id, max, sets, reps, percent_max_weight, rest_secs) 
                                                    VALUES (:workout_id, :exercise_id, :max, :sets, :reps, :percent_max_weight, :rest_secs) RETURNING id"""), {
                                                        'workout_id': new_step.workout_id,
                                                        'exercise_id': new_step.exercise_id,
                                                        'max': new_step.max,
                                                        'sets': new_step.sets,
                                                        'reps': new_step.reps,
                                                        'percent_max_weight': new_step.percent_max_weight,
                                                        'rest_secs': new_step.rest_secs,
                                                    }).scalar_one()
        return {'new_step_id': id}
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")




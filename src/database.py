import os
import dotenv
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()
    print(os.environ.get("POSTGRES_URI"))

    return os.environ.get("POSTGRES_URI")



engine = create_engine("postgresql://postgres:gym-app-native@db.cakcjbjqkmhabjtjnoar.supabase.co:5432/postgres", pool_pre_ping=True)
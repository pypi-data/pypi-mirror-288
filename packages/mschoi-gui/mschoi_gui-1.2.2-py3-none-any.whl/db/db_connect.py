from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import getenv, path
import pyodbc

from ..dir.dir_management import find_project_root


def get_connect_string(db_name):
    root_path = find_project_root()
    env_path = path.join(root_path, 'config', '.env')
    load_dotenv(env_path)

    driver = getenv('DB_DRIVER')
    server = getenv('DB_HOST')
    uid = getenv('DB_USER')
    pwd = getenv('DB_PASSWORD')
    
    connect_string = (
        f"DRIVER={driver};" 
        f"SERVER={server};"
        f"DATABASE={db_name};"
        f"UID={uid};"
        f"PWD={pwd}"
        )
    return connect_string


def make_engine(db_name):
    connection_string =  get_connect_string(db_name)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
    return engine
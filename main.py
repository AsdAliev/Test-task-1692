import os
from dotenv import load_dotenv
from db import DB
from api import TaigaAPI


def upload_all_tables():
    req = TaigaAPI(TAIGA_TOKEN)
    db = DB(host=DB_HOST, database=DB_DATABASE, password=DB_PASSWORD, username=DB_USERNAME)
    db.delete_tables()
    db.create_tables()
    db.upload_users_table(req.get("users"))
    db.upload_projects_table(req.get("projects"))
    db.upload_roles_table(req.get("roles"))
    db.upload_epics_table(req.get("epics"))


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        TAIGA_TOKEN = os.environ.get("TAIGA_TOKEN")
        DB_HOST = os.environ.get("DB_HOST")
        DB_DATABASE = os.environ.get("DB_DATABASE")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_USERNAME = os.environ.get("DB_USERNAME")
    else:
        exit(1)

    upload_all_tables()

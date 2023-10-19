import os
from dotenv import load_dotenv
from db import DB
from api import TaigaAPI


def upload_all_tables(username, password):
    req = TaigaAPI()
    req.auth(username=username, password=password)
    db = DB(host=DB_HOST, database=DB_DATABASE, password=DB_PASSWORD, username=DB_USERNAME)
    db.create_tables()
    db.upload_users_table(req.get("users"))
    db.upload_projects_table(req.get("projects"))
    db.upload_roles_table(req.get("roles"))
    db.upload_epics_table(req.get("epics"))


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        DB_HOST = os.environ.get("DB_HOST")
        DB_DATABASE = os.environ.get("DB_DATABASE")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_USERNAME = os.environ.get("DB_USERNAME")
        TAIGA_USERNAME = os.environ.get("TAIGA_USERNAME")
        TAIGA_PASSWORD = os.environ.get("TAIGA_PASSWORD")
        # TAIGA_TOKEN = os.environ.get("TAIGA_TOKEN")
    else:
        print("Добавьте файл '.env' со всеми необходимыми переменными среды")
        exit(1)

    upload_all_tables(TAIGA_USERNAME, TAIGA_PASSWORD)
    print("Все таблицы и записи были добавлены в базу данных!")

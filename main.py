import requests
import json
import os
from dotenv import load_dotenv
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import MetaData, create_engine


class DB:
    def __init__(self, host="95.165.139.93", database="asdb", password="", username="postgres", port="",
                 dialect="postgresql", driver="psycopg2"):
        self.engine = create_engine(
            "{}+{}://{}:{}@{}{}/{}".format(dialect, driver, username, password, host, port, database))
        self.metadata = MetaData()
        self.users = Table("users", self.metadata,
                           Column("id", Integer(), primary_key=True),
                           Column("username", String(100), nullable=False),
                           Column("full_name", String(200), nullable=False),
                           Column("full_name_display", String(200), nullable=False),
                           Column("color", String(50), nullable=False),
                           Column("bio", String(200)),
                           Column("lang", String(10)),
                           Column("theme", String(50)),
                           Column("photo", String(200)),
                           Column("gravatar_id", String(400), nullable=False)
                           )
        self.projects = Table("projects", self.metadata,
                              Column("id", Integer(), primary_key=True),
                              Column("name", String(200), nullable=False),
                              Column("slug", String(50), nullable=False),
                              Column("description", String(300), nullable=False),
                              Column("created_date", DateTime(), nullable=False),
                              Column("owner_id", ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
                              )
        self.roles = Table("roles", self.metadata,
                           Column("id", Integer(), primary_key=True),
                           Column("name", String(200), nullable=False),
                           Column("slug", String(100), nullable=False),
                           Column("order", Integer(), nullable=False),
                           Column("computable", Boolean(), nullable=False),
                           Column("members_count", Integer(), nullable=False),
                           Column("project_id", ForeignKey("projects.id", ondelete='CASCADE'), nullable=False)
                           )
        self.project_members = Table("project_members", self.metadata,
                                     Column("user_id", Integer(),
                                            ForeignKey("users.id", ondelete='CASCADE'), primary_key=True),
                                     Column("project_id", Integer(), ForeignKey("projects.id", ondelete='CASCADE'),
                                            primary_key=True),
                                     Column("role", Integer(), ForeignKey("roles.id", ondelete="CASCADE"))
                                     )
        self.epics = Table("epics", self.metadata,
                           Column("id", Integer(), primary_key=True),
                           Column("ref", Integer(), nullable=False),
                           Column("status", Integer(), nullable=False),
                           Column("created_date", DateTime(), nullable=False),
                           Column("subject", String(100), nullable=False),
                           Column("project_id", ForeignKey("projects.id", ondelete='CASCADE'), nullable=False),
                           Column("owner_id", ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
                           )

    def upload_db(self, data):
        pass

    def create_tables(self):
        self.metadata.create_all(self.engine)

    def delete_tables(self):
        self.metadata.drop_all(self.engine)


class TaigaAPI:
    def __init__(self, token, host="https://track.miem.hse.ru", token_type="Bearer"):
        self.url = host + "/api/v1/"
        self.params = {}
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "{} {}".format(token_type, token)
        }

    def get(self, obj, pagination=False, page=1, page_size=100):
        self.url += obj
        if pagination:
            self.params["page"] = str(page)
            self.params["page_size"] = str(page_size)
        else:
            self.headers["x-disable-pagination"] = "True"
        r = requests.get(self.url, params=self.params, headers=self.headers)
        try:
            r.raise_for_status()
            if 200 <= r.status_code < 300:
                # Will be deleted
                with open("info.json", "w", encoding="utf-8") as f:
                    json.dump(r.json(), f, indent=2, ensure_ascii=False)
                #
                return r
        except requests.HTTPError as err:
            print(f"HTTP error occured: {err}")

    def get_users(self):
        r = self.get(obj="/users")
        return r.json()

    def get_projects(self):
        r = self.get(obj="/projects")
        return r.json()

    def get_roles(self):
        r = self.get(obj="/roles")
        return r.json()

    def get_epics(self):
        r = self.get(obj="/epics")
        return r.json()


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        TOKEN = os.environ.get('TOKEN')
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
    else:
        exit(1)

    req = TaigaAPI(TOKEN)
    users = req.get_users()
    with open("info.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    mydb = DB(password=DB_PASSWORD)
    mydb.delete_tables()

from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import MetaData, create_engine


class DB:
    def __init__(self, host="localhost", database="name", password="pass", username="postgres", port="",
                 dialect="postgresql", driver="psycopg2"):
        self.__engine = create_engine(
            "{}+{}://{}:{}@{}{}/{}".format(dialect, driver, username, password, host, port, database))
        self.__metadata = MetaData()
        self.__users = Table("users", self.__metadata,
                             Column("id", Integer(), primary_key=True),
                             Column("username", String(100), nullable=False),
                             Column("full_name", String(100), nullable=False),
                             Column("full_name_display", String(100), nullable=False),
                             Column("color", String(20), nullable=False),
                             Column("bio", String(300)),
                             Column("lang", String(2)),
                             Column("theme", String(10)),
                             Column("photo", String(400)),
                             Column("gravatar_id", String(50), nullable=False)
                             )
        self.__projects = Table("projects", self.__metadata,
                                Column("id", Integer(), primary_key=True),
                                Column("name", String(200), nullable=False),
                                Column("slug", String(200), nullable=False),
                                Column("description", String(3000), nullable=False),
                                Column("created_date", DateTime(), nullable=False),
                                # owner_id не foreign_key, так как некоторые пользователи были удалены
                                Column("owner_id", Integer(), nullable=False)
                                )
        self.__roles = Table("roles", self.__metadata,
                             Column("id", Integer(), primary_key=True),
                             Column("name", String(200), nullable=False),
                             Column("slug", String(200), nullable=False),
                             Column("order", Integer(), nullable=False),
                             Column("computable", Boolean(), nullable=False),
                             Column("members_count", Integer(), nullable=False),
                             Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
                             )

        self.__epics = Table("epics", self.__metadata,
                             Column("id", Integer(), primary_key=True),
                             Column("ref", Integer(), nullable=False),
                             Column("status", Integer(), nullable=False),
                             Column("created_date", DateTime(), nullable=False),
                             Column("subject", String(200), nullable=False),
                             Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
                             # owner_id не foreign_key, так как некоторые пользователи были удалены
                             Column("owner_id", Integer(), nullable=False)
                             )

    def __upload_table(self, table, data):
        t_insert = table.insert().values(data)
        conn = self.__engine.connect()
        t_delete = table.delete()
        conn.execute(t_delete)
        conn.execute(t_insert)
        conn.commit()

    def upload_users_table(self, data_list):
        data = []
        for value in data_list:
            data.append(
                {
                    "id": value["id"],
                    "username": value["username"],
                    "full_name": value["full_name"],
                    "full_name_display": value["full_name_display"],
                    "color": value["color"],
                    "bio": value["color"],
                    "lang": value["lang"],
                    "theme": value["theme"],
                    "photo": value["photo"],
                    "gravatar_id": value["gravatar_id"]}
            )
        self.__upload_table(self.__users, data)

    def upload_projects_table(self, data_list):
        data = []
        for value in data_list:
            data.append(
                {
                    "id": value["id"],
                    "name": value["name"],
                    "slug": value["slug"],
                    "description": value["description"],
                    "created_date": value["created_date"],
                    "owner_id": value["owner"]["id"]
                }
            )
        self.__upload_table(self.__projects, data)

    def upload_roles_table(self, data_list):
        data = []
        for value in data_list:
            data.append(
                {
                    "id": value["id"],
                    "name": value["name"],
                    "slug": value["slug"],
                    "order": value["order"],
                    "computable": value["computable"],
                    "members_count": value["members_count"],
                    "project_id": value["project"]
                }
            )
        self.__upload_table(self.__roles, data)

    def upload_epics_table(self, data_list):
        data = []
        for value in data_list:
            data.append(
                {
                    "id": value["id"],
                    "ref": value["ref"],
                    "status": value["status"],
                    "created_date": value["created_date"],
                    "subject": value["subject"],
                    "project_id": value["project"],
                    "owner_id": value["owner"]
                }
            )
        self.__upload_table(self.__epics, data)

    def get_db(self, table_name):
        conn = self.__engine.connect()
        match table_name:
            case "users":
                table = self.__users
            case "projects":
                table = self.__projects
            case "roles":
                table = self.__roles
            case "epics":
                table = self.__epics
            case _:
                table = self.__users
        s = table.select()
        r = conn.execute(s)
        return r.fetchall()

    def create_tables(self):
        self.__metadata.create_all(self.__engine)

    def delete_tables(self):
        self.__metadata.drop_all(self.__engine)

from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import MetaData, create_engine


class DB:
    def __init__(self, host="localhost", database="name", password="pass", username="postgres", port="",
                 dialect="postgresql", driver="psycopg2"):
        self.engine = create_engine(
            "{}+{}://{}:{}@{}{}/{}".format(dialect, driver, username, password, host, port, database))
        self.metadata = MetaData()
        self.users = Table("users", self.metadata,
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
        self.projects = Table("projects", self.metadata,
                              Column("id", Integer(), primary_key=True),
                              Column("name", String(200), nullable=False),
                              Column("slug", String(200), nullable=False),
                              Column("description", String(3000), nullable=False),
                              Column("created_date", DateTime(), nullable=False),
                              # owner_id не foreign_key, так как некоторые пользователи были удалены
                              Column("owner_id", Integer(), nullable=False)
                              )
        self.roles = Table("roles", self.metadata,
                           Column("id", Integer(), primary_key=True),
                           Column("name", String(200), nullable=False),
                           Column("slug", String(200), nullable=False),
                           Column("order", Integer(), nullable=False),
                           Column("computable", Boolean(), nullable=False),
                           Column("members_count", Integer(), nullable=False),
                           Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
                           )
        self.project_members = Table("project_members", self.metadata,
                                     # user_id не foreign_key, так как некоторые пользователи были удалены
                                     Column("user_id", Integer(), primary_key=True),
                                     Column("project_id", Integer(), ForeignKey("projects.id", ondelete="CASCADE"),
                                            primary_key=True),
                                     Column("role", Integer(), ForeignKey("roles.id", ondelete="CASCADE"))
                                     )
        self.epics = Table("epics", self.metadata,
                           Column("id", Integer(), primary_key=True),
                           Column("ref", Integer(), nullable=False),
                           Column("status", Integer(), nullable=False),
                           Column("created_date", DateTime(), nullable=False),
                           Column("subject", String(200), nullable=False),
                           Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
                           # owner_id не foreign_key, так как некоторые пользователи были удалены
                           Column("owner_id", Integer(), nullable=False)
                           )

    def upload_table(self, table, data):
        t_insert = table.insert().values(data)
        conn = self.engine.connect()
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
        self.upload_table(self.users, data)

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
        self.upload_table(self.projects, data)

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
        self.upload_table(self.roles, data)

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
        self.upload_table(self.epics, data)

    def get_db(self):
        conn = self.engine.connect()

        s = self.users.select()
        r = conn.execute(s)
        print(r.fetchall())

    def create_tables(self):
        self.metadata.create_all(self.engine)

    def delete_tables(self):
        self.metadata.drop_all(self.engine)

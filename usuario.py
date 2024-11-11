from main import *
from sqlalchemy import text, quoted_name, MetaData, engine

with db.connect() as connection:
    DATABASE_USER = "admin"
    DATABASE_USER_PASSWORD = "admin123"

    create_user_sql = text(f"CREATE USER '{DATABASE_USER}'@'localhost' IDENTIFIED BY '{DATABASE_USER_PASSWORD}';")
    result = connection.execute(create_user_sql)

    for row in result:
        print(row)

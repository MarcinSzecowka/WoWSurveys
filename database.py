from os import environ

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


databaseHost = environ.get("DB_HOST", "localhost:5432")
databaseName = environ.get("DB_NAME", "wowsurveysdb")
databaseUser = environ.get("DB_USER", "wowsurveys")
databasePassword = environ.get("DB_PASSWORD", "wowsurveyspass")
db_socket_dir = environ.get("DB_SOCKET_DIR", "")
cloud_sql_connection_name = environ.get("DB_CONNECTION_NAME")
is_cloud_env = environ.get("GAE_ENV")

engine = None
if is_cloud_env:
    engine = create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgres",
            username=databaseUser,
            password=databasePassword,
            database=databaseName,
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,
                    cloud_sql_connection_name)
            }
        ),
    )
else:
    DATABASE_URL = f"postgresql://{databaseUser}:{databasePassword}@{databaseHost}/{databaseName}"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

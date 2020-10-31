from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

databaseHost = environ.get("DB_HOST", "localhost:5432")
databaseName = environ.get("DB_NAME", "wowsurveysdb")
databaseUser = environ.get("DB_USER", "wowsurveys")
databasePassword = environ.get("DB_PASSWORD", "wowsurveyspass")

DATABASE_URL = f"postgresql://{databaseUser}:{databasePassword}@{databaseHost}/{databaseName}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

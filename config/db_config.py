from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import logging

username = "postgres"
password = quote_plus("Password123#@!")
host = quote_plus("localhost")
port = quote_plus("5432")
database = quote_plus("library_ms")

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Log a message to indicate that the database is connected
logging.info("Database connected successfully")

# Create a MetaData object
metadata_obj = MetaData()

# Associate the MetaData object with the declarative_base
Base = declarative_base(metadata=metadata_obj)

# Bind the engine to the MetaData object when defining tables
metadata_obj.create_all(bind=engine)

# Create a sessionmaker that will use the engine
# SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#LOCAL_VERSION
# import os
# from pathlib import Path
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import dotenv_values
# #build absolute path to .env file and load it into memory
# BASE_DIR = Path(__file__).resolve().parent.parent
# env_path = os.path.join(BASE_DIR, ".env")
# env_config = dotenv_values(env_path)

# #get the database 
# SQLALCHEMY_DATABASE_URL = env_config.get("DATABASE_URL")
# if not SQLALCHEMY_DATABASE_URL:
#     raise ValueError(f"\n🛑 CRITICAL ERROR: DATABASE_URL is missing!\nPython looked for your .env file exactly here: {env_path}\nPlease ensure the file exists at that exact path and contains 'DATABASE_URL=...'\n")
# #engine is the actual connection to the database
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# #temporary session factory for creating database sessions
# session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# #use the Base class that User model inherits from to create the database tables
# Base = declarative_base()
# #safly open and close the database using this function
# def get_db():
#     db = session_local()
#     try:
#         yield db
#     finally:
#         db.close()
#DEPLOY_VERSION
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Look for the Render URL, fallback to local SQLite if it doesn't exist
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# 2. Fix the Render Postgres URL format if necessary
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Create the engine (SQLite needs special arguments, Postgres does not)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

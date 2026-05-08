from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

#This creates a local SQLite database file called taskmanager.db
DATABASE_URL = "sqlite:///./taskmanager.db"

# Engine connects SQLAlchemy to the database
engine = create_engine ( DATABASE_URL, connect_args={"check_same_thread" : False} ) 

#Each request gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
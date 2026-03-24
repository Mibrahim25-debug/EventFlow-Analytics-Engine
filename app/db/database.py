from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Database_URL = 'sqlite:///./event_analytics.db'

engine = create_engine(Database_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()




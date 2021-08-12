from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, Depends, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()

'''
temporarily using SQLite database for local development
SQLALCHEMY_DATABASE_URL = dialect://user:password@host.dbname
'''

#connect to ElephantSQL-hosted PostgreSQL
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

DATABASE_URL = 'postgresql://{}:{}@{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

class Stories(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    story = Column(String, index=True)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_story(db: Session, id: int):
    return db.query(Stories).filter(Stories.id == id).first()

@router.get('/storytext')
def show_story(id: int, db: Session = Depends(get_db)):
    db_story = get_story(db, id=id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found, id must be between 1-167")
    return db_story


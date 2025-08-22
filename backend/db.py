from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:password@localhost:5432/backdb"

engine = create_engine(DATABASE_URL) # this is the SQL engine
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # this creates the SQL session that I operate with
Base = declarative_base() # this is the base class for models

class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    review = Column(String)

def initialize_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:password@localhost:5432/backdb"

engine = create_engine(DATABASE_URL) # this is the SQL engine
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # this creates the SQL session that I operate with
Base = declarative_base() # this is the base class for models

class Website(BaseModel):
    name: str
    link: str
    review: str | None = None

class Data(BaseModel):
    name: str
    filename: str
    rows: int | None = None
    cols: int | None = None
    status: str # processing, done, error

class WebsiteTable(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    review = Column(String)

class DataTable(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True, unique=True)
    filename = Column(String, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.now)
    rows = Column(Integer)
    cols = Column(Integer)
    status = Column(String, nullable=False, default="processing") # processing, done, error

class ModelTable(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False, index=True)
    done = Column(Boolean, default=False, nullable=False)

    

def initialize_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_data(dat: Data, db: Session):
    data = DataTable(name=dat.name, filename=dat.filename, rows=dat.rows or 0, cols=dat.cols or 0, status=dat.status or "processing")
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def update_data(dat: Data, db: Session):
    data = db.query(DataTable).filter(DataTable.name == dat.name).first()
    if data:
        data.rows = dat.rows or data.rows
        data.cols = dat.cols or data.cols
        data.status = dat.status or data.status
        db.commit()
        db.refresh(data)
    return data

def insert_website(site: Website, db: Session):
    website = WebsiteTable(name=site.name, link=site.link, review=site.review)
    db.add(website)
    db.commit()
    db.refresh(website)
    return website
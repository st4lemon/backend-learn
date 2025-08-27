from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
import sqlalchemy
from sqlalchemy import future
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from pydantic import BaseModel
import asyncpg
import psycopg2

DATABASE_URL = "://postgres:password@localhost:5432/backdb"

engine = create_engine(f"postgresql+psycopg2{DATABASE_URL}") # this is the SQL engine
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # this creates the SQL session that I operate with
Base = declarative_base() # this is the base class for models

async_engine = create_async_engine(f"postgresql+asyncpg{DATABASE_URL}", echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)



class Website(BaseModel):
    name: str
    link: str
    review: str | None = None

class Data(BaseModel):
    name: str
    filename: str
    rows: int | None = None
    cols: int | None = None
    status: str = "processing" # processing, done, error
    error: str | None = None

class Model(BaseModel):
    name: str | None = None
    datafile: str | None = None
    algorithm: str | None = None

class Sample(BaseModel):
    data_name: str
    features: list[float]

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
    status = Column(String(16), nullable=False, default="processing") # processing, done, error
    error = Column(String, default="")

    models = relationship("ModelTable", back_populates="data")

class ModelTable(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    datafile = Column(String, ForeignKey('data.name'))
    created = Column(DateTime, nullable=False, default=datetime.now)
    algorithm = Column(String, nullable=False)

    data = relationship("DataTable", back_populates="models")


def initialize_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

async def get_async_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def insert_data(dat: Data, db: AsyncSession):
    data = DataTable(name=dat.name, filename=dat.filename, rows=dat.rows or 0, cols=dat.cols or 0, status=dat.status or "processing")
    db.add(data)
    try:
        await db.commit()
        await db.refresh(data)
        return data
    except IntegrityError as e:
        await db.rollback()
        print("Duplicate entry:", e)
        return None

async def update_data(dat: Data, db: AsyncSession):
    stmt = future.select(DataTable).filter(DataTable.name == dat.name)
    data = (await db.execute(stmt)).scalars().first()
    if data:
        data.rows = dat.rows or data.rows
        data.cols = dat.cols or data.cols
        data.status = dat.status or data.status
        data.error = dat.error or data.error
        await db.commit()
        await db.refresh(data)
    return data

def insert_model(mod: Model, db: Session):
    model = ModelTable(name=mod.name, datafile=mod.datafile, algorithm=mod.algorithm)
    db.add(model)
    try:
        db.commit()
        db.refresh(model)
        return model
    except IntegrityError as e:
        db.rollback()
        print("Duplicate entry:", e)
        return None

def insert_website(site: Website, db: Session):
    website = WebsiteTable(name=site.name, link=site.link, review=site.review)
    db.add(website)
    db.commit()
    db.refresh(website)
    return website

def get_all_data(db: Session):
    res = db.execute(sqlalchemy.select(DataTable.name, DataTable.rows, DataTable.cols, DataTable.status, DataTable.error)).all()
    
    return [dict(r._mapping) for r in res]

def get_by_name(name: str, db: Session):
    stmt = sqlalchemy.select(DataTable.name, DataTable.rows, DataTable.cols, DataTable.status, DataTable.error).where(DataTable.name == name)
    res = db.execute(stmt).all()
    
    return [dict(r._mapping) for r in res]
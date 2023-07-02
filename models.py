from sqlalchemy import Column, JSON, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/netology'

engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class SwapiPeople(Base):

    __tablename__ = 'swapi_people'

    # json = Column(JSON)
    id = Column(Integer, primary_key=True)
    birth_year = Column(String(25))
    eye_color = Column(String(25))
    films = Column(String(1000))
    gender = Column(String(25))
    hair_color = Column(String(25))
    height = Column(String(25))
    homeworld = Column(String(50))
    mass = Column(String(25))
    name = Column(String(50))
    skin_color = Column(String(50))
    species = Column(String(1000))
    starships = Column(String(1000))
    vehicles = Column(String(1000))
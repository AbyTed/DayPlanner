import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ActivitySchedule(Base):
    __tablename__ = "schedule"

    name = Column(String, nullable=False, primary_key=True, unique=True)
    time = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    break_time = Column(Integer)


engine = create_engine("sqlite:///day_planner.db")

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session instance
session = Session()




import model
from config import settings

from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy.engine.base import Engine

def create_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)
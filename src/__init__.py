from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///src/sqlite3.db', echo=True)
Base = declarative_base()


from .models import *

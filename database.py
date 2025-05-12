from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Criação do arquivo SQLite local chamado tracking.db
engine = create_engine('sqlite:///tracking.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

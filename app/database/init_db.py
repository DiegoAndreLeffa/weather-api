from app.database.connection import engine
from app.models.weather import Base


def init_database():
    Base.metadata.create_all(bind=engine)
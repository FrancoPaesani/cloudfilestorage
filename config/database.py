from sqlalchemy import MetaData
from sqlmodel import Session, create_engine

from config.utils import DB_SCHEMA, DB_URL

engine = create_engine(DB_URL)

CFS_METADATA = MetaData(schema=DB_SCHEMA)


def get_session():
    with Session(engine) as session:
        yield session

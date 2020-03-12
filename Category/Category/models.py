from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL



DeclarativeBase = declarative_base()


def db_connect():
  
    return create_engine("postgresql://kayn:starvn66@localhost/ComicCrawler")


def create_deals_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Category(DeclarativeBase):
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True)
    categoryName = Column(String)
    categoryLink = Column(String)
import datetime
from sqlalchemy.orm import DeclarativeBase, relationship, declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    BigInteger
)


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Source(Base):

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)


class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    url = Column(String)

    source_id = Column(Integer, ForeignKey("sources.id"))

    published_at = Column(DateTime)

    source = relationship("Source")


class Subscription(Base):

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))

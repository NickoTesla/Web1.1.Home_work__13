from sqlalchemy import Column, Integer, String, Boolean, Date

from sqlalchemy.ext.declarative import declarative_base

from datetime import date

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship


Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    additional_data = Column(String)
    created_at: Mapped[date] = Column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = Column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable = True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50))
    email: Mapped[str] = Column(String(250), nullable=False, unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)
    created_at: Mapped[date] = Column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    avatar: Mapped[str] = Column(String(255), nullable=True)
    refresh_token: Mapped[str] = Column(String(255), nullable=True)


# Base.metadata.create_all(bind=engine)


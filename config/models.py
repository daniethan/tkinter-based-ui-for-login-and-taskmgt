from .dbconfig import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dt

class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    pin = Column(String(5), nullable=False)
    # created_at = Column(DateTime, server_default=dt.utcnow)

    device = relationship('Device', back_populates='owner')

class Device(Base):
    __tablename__ = 'device'
    uid = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(120), unique=True, nullable= False)
    userId = Column(Integer, ForeignKey('user.uid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    owner = relationship('User', back_populates='device')
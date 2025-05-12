from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # 'admin' ou 'client'

class Package(Base):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    origin_city = Column(String)
    dest_city = Column(String)
    is_tracked = Column(Boolean, default=False)

class TrackingRoute(Base):
    __tablename__ = 'tracking_route'
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    city = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

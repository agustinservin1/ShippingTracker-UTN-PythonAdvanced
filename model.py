from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum
from datetime import datetime
from typing import List, Union


DATABASE_URL = "sqlite:///shipping.db" 
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class ShippingState(enum.Enum):
    CREATED = "Created"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    RETURNED = "Returned"

# Modelo de la tabla Shipping
class Shipping(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    sender_address = Column(Text, nullable=False)
    recipient_address = Column(Text, nullable=False)
    current_state = Column(Enum(ShippingState), nullable=False, default=ShippingState.CREATED)
    location = Column(String(100), nullable=True)

    states = relationship("State", back_populates="shipping", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (f"<Shipping(id={self.id}, tracking_number={self.tracking_number}, "
                f"state={self.current_state}, location={self.location})>")

# State table model
class State(Base):

     __tablename__ = 'states'

     id = Column(Integer, primary_key=True, autoincrement=True)
     shipping_id = Column(Integer, ForeignKey('shipments.id'))
     state = Column(Enum(ShippingState), nullable=False)
     location = Column(String(100), nullable=False)
     timestamp = Column(DateTime, default=datetime.utcnow)
     shipping = relationship("Shipping", back_populates="states") def __repr__(self) -> str: return f"<State(state={self.state}, location={self.location},

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

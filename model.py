from sqlalchemy import create_engine, Column, Integer, String, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

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

    def __repr__(self):
        return (f"<Shipping(id={self.id}, tracking_number={self.tracking_number}, "
                f"state={self.current_state}, location={self.location})>")

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

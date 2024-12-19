from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from src.database.database import Base 
class Shipping(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    sender_address = Column(Text, nullable=False)
    recipient_address = Column(Text, nullable=False)
    current_state = Column(String(20), nullable=False)
    location = Column(String(100))
    is_active = Column(Boolean, default=True) 

    states = relationship("State", back_populates="shipping", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (f"Shipping(id={self.id}, tracking_number={self.tracking_number}, "
                f"state={self.current_state}, location={self.location}, is_active={self.is_active})")
    
    def to_dict(self):
        return {
            "id": self.id,
            "tracking_number": self.tracking_number,
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "current_state": self.current_state,
            "location": self.location,
            "is_active": self.is_active
        }
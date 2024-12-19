from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from src.database.database import Base

class State(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True, index=True)
    shipping_id = Column(Integer, ForeignKey('shipments.id'), nullable=False)
    state = Column(String(20), nullable=False)
    location = Column(String(100), nullable=False)
    distance = Column(Integer, nullable=False, default=1)
    weight = Column(Integer, nullable=False, default=1)
    timestamp = Column(DateTime, default=func.now(), nullable=False)

    shipping = relationship("Shipping", back_populates="states")

    def __repr__(self) -> str:
        return f"State(id={self.id}, state={self.state}, location={self.location})"

    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "location": self.location,
            "distance": self.distance,
            "weight": self.weight,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

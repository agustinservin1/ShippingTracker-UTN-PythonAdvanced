from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models import Shipping
from src.models.schemas import PackageRequest

class ShippingService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_package(self, tracking_number: str) -> Shipping:
        package = self.db.query(Shipping).filter_by(tracking_number=tracking_number).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        return package

    def get_all_packages(self) -> List[Shipping]:
        return self.db.query(Shipping).all()

    def create_package(self, request: PackageRequest) -> Shipping:
        try:
            package = Shipping(
                tracking_number=request.tracking_number,
                sender_address=request.sender_address,
                recipient_address=request.recipient_address,
                current_state="CREATED"  
            )
            self.db.add(package)
            self.db.commit()
            self.db.refresh(package)
            return package
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

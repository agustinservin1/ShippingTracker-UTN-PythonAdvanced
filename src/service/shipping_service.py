from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models import Shipping
from src.models.schemas import PackageRequest,PackageUpdateRequest
from src.utils.email_service.email_service import EmailService
from src.utils.observer.subject import ObservableEntity 
from src.utils.observer.observers import EmailObserver

class ShippingService(ObservableEntity):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__()
        self.db = db
        self.add_observer(EmailObserver()) 

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
                current_state="CREATED",  
                email=request.email
            )
            self.db.add(package)
            self.db.commit()
            self.db.refresh(package)
            self.notify_observers("CREATE", package)  
            return package
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        
    def update_package(self, package_id: int, request: PackageUpdateRequest) -> Shipping:
        package = self.db.query(Shipping).filter_by(id=package_id).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        package.sender_address = request.sender_address
        package.recipient_address = request.recipient_address
        package.email = request.email
        self.db.commit()
        self.db.refresh(package)
        self.notify_observers("UPDATE", package)
        return package
    
    def delete_logic_package(self, package_id: int) -> Shipping: 
        package = self.db.query(Shipping).filter_by(id=package_id, is_active=True).first()
        if not package: 
            raise HTTPException(status_code=404, detail="Package not found") 
        package.is_active = False 
        self.db.commit()
        return package
        
    def delete_package(self, package_id: int) -> Shipping:
        package = self.db.query(Shipping).filter_by(id=package_id).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        self.db.delete(package)
        self.db.commit()
        return package
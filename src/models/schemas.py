from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PackageRequest(BaseModel):
    tracking_number: str = Field(..., description="Unique tracking number for the package")
    sender_address: str = Field(..., description="Address of the sender")
    recipient_address: str = Field(..., description="Address of the recipient")

    class Config:
        json_schema_extra = {
            "example": {
                "tracking_number": "TRK123456789",
                "sender_address": "123 Sender St, City, Country",
                "recipient_address": "456 Recipient Ave, City, Country"
            }
        }
        
class PackageUpdateRequest(BaseModel):
    sender_address: str = Field(..., description="Address of the sender")
    recipient_address: str = Field(..., description="Address of the recipient")

    class Config:
        json_schema_extra = {
            "example": {
                "sender_address": "123 Sender St, City, Country",
                "recipient_address": "456 Recipient Ave, City, Country"
            }
        }

class StateRequest(BaseModel):
    package_id: int = Field(..., description="ID of the package")
    location: str = Field(..., description="Current location of the package")
    distance: int = Field(..., ge=1, description="Distance traveled")
    weight: int = Field(..., ge=1, description="Weight of the package")

    class Config:
        json_schema_extra = {
            "example": {
                "package_id": 1,
                "location": "Distribution Center A",
                "distance": 100,
                "weight": 5
            }
        }

class ShippingResponse(BaseModel):
    id: int
    tracking_number: str
    current_state: str
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

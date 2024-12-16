from pydantic import BaseModel
from src.models.db_models import ShippingState

class PackageRequest(BaseModel):
    tracking_number: str
    sender_address: str
    recipient_address: str

class StateRequest(BaseModel):
    package_id: int
    #state: ShippingState
    location: str
    distance: int = 1
    weight: int = 1

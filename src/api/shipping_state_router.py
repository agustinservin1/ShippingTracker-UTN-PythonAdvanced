from fastapi import APIRouter, Depends, Query
from src.service.shipping_state_service import ShippingStateService
from src.models.schemas import StateRequest
from src.models.shipping_state import ShippingState

router = APIRouter(prefix="/shipping-state", tags=["Shipping State"])

@router.get("/package/{tracking_number}/states")
def get_package_states(tracking_number: str, service: ShippingStateService = Depends()):
    return {"states": service.get_package_states(tracking_number)}

@router.post("/add_state")
def add_state(request: StateRequest, state: ShippingState = Query(...), service: ShippingStateService = Depends()):
    return {"state": service.add_state(request, state)}

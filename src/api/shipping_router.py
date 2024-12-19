from fastapi import APIRouter, Depends
from src.service.shipping_service import ShippingService
from src.models.schemas import PackageRequest

router = APIRouter(prefix="/shipping", tags=["Shipping"])

@router.get("/package/{tracking_number}")
def get_package(tracking_number: str, service: ShippingService = Depends()):
    return {"package": service.get_package(tracking_number)}

@router.get("/packages")
def get_all_packages(service: ShippingService = Depends()):
    return {"packages": service.get_all_packages()}

@router.post("/create_package")
def create_package(request: PackageRequest, service: ShippingService = Depends()):
    return {"message": service.create_package(request)}

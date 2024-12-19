from fastapi import APIRouter, Depends
from src.service.shipping_service import ShippingService
from src.models.schemas import PackageRequest, PackageUpdateRequest

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

@router.put("/update_package/{package_id, package_request}")
def update_package(package_id: int, package_request: PackageUpdateRequest, service: ShippingService = Depends()):
     return {"message": service.update_package(package_id, package_request)}

@router.put("/delete_logic_package")
def delete_logic_package(package_id: int, service: ShippingService = Depends()):
    return {"message": service.delete_logic_package(package_id)}
@router.delete("/delete_package")
def delete_package(package_id: int, service: ShippingService = Depends()):
       return {"message":  service.delete_package(package_id)}


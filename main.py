from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from controller import ShippingController

app = FastAPI(
    title="Shipping Tracker API",
    description="Documentación interactiva para la API de gestión de envíos.",
    version="1.0.0"
    )
controller = ShippingController()

class PackageRequest(BaseModel):
    tracking_number: str
    sender_address: str
    recipient_address: str

class StateRequest(BaseModel):
    package_id: int
    state: str
    location: str
    distance: int = 1
    weight: int = 1


@app.post("/create_package")
def create_package(request: PackageRequest):
    result = controller.create_package(
        tracking_number=request.tracking_number,
        sender_address=request.sender_address,
        recipient_address=request.recipient_address
    )
    if "Error" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"message": result}

@app.post("/add_state")
def add_state(request: StateRequest):
    result = controller.add_state(
        package_id=request.package_id,
        state=request.state,
        location=request.location,
        distance=request.distance,
        weight=request.weight
    )
    if "Error" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"message": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

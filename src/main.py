from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from src.controllers.controller import ShippingController
from src.models.request_models import PackageRequest, StateRequest
from src.models.db_models import ShippingState

app = FastAPI(
    title="Shipping Tracker API",
    description="Documentación interactiva para la API de gestión de envíos.",
    version="1.0.0"
    )
controller = ShippingController()
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
     return JSONResponse(
           status_code=500,
           content={"message": str(exc)
            })

@app.get("/package/{tracking_number}")
def get_package(tracking_number: str):
    result = controller.get_package(tracking_number)
    if "Error" in result:
        raise HTTPException(status_code=404, detail=result)
    return {"package": result}

@app.get("/package/{tracking_number}/states")
def get_package_states(tracking_number: str):
    result = controller.get_package_states(tracking_number)
    if "Error" in result:
        raise HTTPException(status_code=404, detail=result)
    return {"states": result}

@app.get("/packages")
def get_all_packages():
    result = controller.get_all_packages()
    return {"packages": result}

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
def add_state(
    request:StateRequest,
    state: ShippingState = Query(...) 
    ):
    try:
        state_value = state.value
        result = controller.add_state(
            package_id=request.package_id,
            state=state_value,
            location=request.location,
            distance=request.distance,
            weight=request.weight
        )
        if "Error" in result:
            raise HTTPException(status_code=400, detail=result)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

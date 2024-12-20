from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.shipping_router import router as shipping_router
from src.api.shipping_state_router import router as shipping_state_router
from src.database.database import engine, Base
from src.core.exceptions import ShippingException
from src.utils.observer.observers import EmailObserver  
from src.service.shipping_service import ShippingService
from src.service.shipping_state_service import   ShippingStateService
from dotenv import load_dotenv

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shipping Tracker API",
    description="API for managing package shipments and tracking their states",
    version="1.0.0",
    docs_url="/", 
    redoc_url="/redoc"  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shipping_service = ShippingService()
shipping_state_service = ShippingStateService()

email_observer = EmailObserver()
shipping_service.add_observer(email_observer)
shipping_state_service.add_observer(email_observer)

app.include_router(shipping_router, prefix="/shipping", tags=["Shipping"])
app.include_router(shipping_state_router, prefix="/shipping-state", tags=["Shipping State"])
@app.exception_handler(ShippingException)
async def shipping_exception_handler(request: Request, exc: ShippingException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Welcome to the Shipping Tracker API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

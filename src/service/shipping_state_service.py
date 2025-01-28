from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models import State, Shipping, ShippingState
from src.models.schemas import StateRequest
from src.utils.observer.subject import ObservableEntity 
from src.utils.observer.observers import EmailObserver
from src.utils.decorators import calculate_costs
from src.config.logging_config import LOG_CLIENT_CONFIG  
from src.api.dependencies import get_log_client 
from src.utils.logging.log_client import LogClient

class ShippingStateService(ObservableEntity):
    def __init__(
            self, db: Session = Depends(get_db),
                        log_client: LogClient = Depends(get_log_client)):
        
        super().__init__()  
        self.db = db
        self.log_client = log_client 

        self.add_observer(EmailObserver())

    def get_package_states(self, tracking_number: str) -> List[dict]:
        
        package = self.db.query(Shipping).filter_by(tracking_number=tracking_number).first()
        
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")

        states = [state.to_dict() for state in package.states]
        
        if not states:
            raise HTTPException(status_code=404, detail="No states found for package")
        return states
    
    #@calculate_cost
    def add_state(self, request: StateRequest, state: str) -> State:
        if not ShippingState.is_valid(state):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid state. Valid states are: {ShippingState.get_values()}"
            )

        try:
            package = self.db.query(Shipping).get(request.package_id)
            if not package:
                raise HTTPException(status_code=404, detail="Package not found")

            state_instance = State(
                shipping=package,
                state=state,
                location=request.location,
                distance=request.distance,
                weight=request.weight
            )
            package.current_state = state
            package.location = request.location

            self.db.add(state_instance)
            self.db.commit()
            self.db.refresh(state_instance)
              
            self.log_client.send_log(
                service="shipping_state",
                message=f"State updated to {state} for package {package.id}",
                level="INFO",
                extra={
                    "package_id": package.id,
                    "new_state": state,
                    "location": request.location
                }
            )
            
            self.notify_observers("UPDATE", state_instance)

            return state_instance.to_summary_dict()

        except Exception as e:
            self.log_client.send_log(
                service="shipping_state",
                message=f"Error updating state: {str(e)}",
                level="ERROR",
                extra={"error_details": str(e)})

            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
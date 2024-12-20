from typing import Union, List
from src.models import Shipping, State
from src.utils.email_service.email_service import EmailService

class Observer:
    def update(self, action: str, data: Union[Shipping, State]) -> None:
            raise NotImplementedError

class EmailObserver(Observer):
    
    def __init__(self):
        self.email_service = EmailService()

    def update(self, action: str, data: Union[Shipping, State]) -> None:
        if isinstance(data, Shipping):
            self._handle_shipping_update(action, data)
        elif isinstance(data, State):
            self._handle_state_update(action, data)

    def _handle_shipping_update(self, action: str, shipping: Shipping) -> None:
        subject = ""
        message = ""
        to_email = shipping.email
        if action == "CREATE":
            subject = f"New Package Created: {shipping.tracking_number}"
            message = f"Package with tracking number {shipping.tracking_number} has been created."    
        elif action == "UPDATE":  
            subject = f"Package Updated: {shipping.tracking_number}"
            message = f"Package with tracking number {shipping.tracking_number} has been updated." 
        
        self.email_service.send_email(to=to_email, subject=subject, message=message)

    def _handle_state_update(self, action: str, state: State) -> None:
        to_email = state.shipping.email
        if action == "UPDATE":
            subject = f"State Updated: {state.shipping.tracking_number}"
            message = (
                f"The state of package {state.shipping.tracking_number} has been updated to {state.state} at location {state.location}."
            )
        self.email_service.send_email(to=to_email, subject=subject, message=message)

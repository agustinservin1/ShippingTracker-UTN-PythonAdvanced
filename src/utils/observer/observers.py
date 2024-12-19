from typing import Union, List
from src.models import Shipping, State
import logging

logger = logging.getLogger(__name__)

class Observer:
    def update(self, action: str, data: Union[Shipping, State]) -> None:
            raise NotImplementedError


class ShippingObserver(Observer):
    def update(self, action: str, data: Union[Shipping, State]) -> None:
        if isinstance(data, Shipping):
            self._handle_shipping_update(action, data)
        elif isinstance(data, State):
            self._handle_state_update(action, data)

    def _handle_shipping_update(self, action: str, shipping: Shipping) -> None:
        if action == "CREATE":
            self._log_notification(f"Package {shipping.tracking_number} was created")
        elif action == "DELETE":
            self._log_notification(f"Package {shipping.tracking_number} was deleted")
 
    def _handle_state_update(self, action: str, state: State) -> None:
        if action == "UPDATE":
            self._log_notification(f"The state of package {state.shipping.tracking_number} changed to {state.state}")

    def _log_notification(self, message: str) -> None:
        logger.info(f"Notification: {message}")

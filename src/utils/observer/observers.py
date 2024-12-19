from typing import Union, List
from src.models import Shipping, State

class Observer:
    def update(self, action: str, data: Union[Shipping, State]) -> None:
            raise NotImplementedError


class StateObserver(Observer):
    def update(self, action: str, data: Union[Shipping, State]) -> None:
        if isinstance(data, Shipping):
            self._handle_shipping_update(action, data)
        elif isinstance(data, State):
            self._handle_state_update(action, data)

    def _handle_shipping_update(self, action: str, shipping: Shipping) -> None:
        if action == "CREATE":
            self._notify(f"Package {shipping.tracking_number} was created")
        elif action == "DELETE":
            self._notify(f"Package {shipping.tracking_number} was deleted")
 
    def _handle_state_update(self, action: str, state: State) -> None:
        if action == "UPDATE":
            self._notify(f"The state of package {state.shipping.tracking_number} changed to {state.state}")

    def _notify(self, message: str) -> None:
        print(f"Notification: {message}")


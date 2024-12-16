from typing import Union
from model import Shipping, State

class StateObserver:

    def update(self, action: str, data: Union[Shipping, State])->None:
        if action == "CREATE":
            print(f"Notification: Package {data.tracking_number} was created")
        elif action == "UPDATE":
            print(f"Notification: The state of package {data.shipping.tracking_number} changed to {data.state}")
        elif action == "DELETE":
            print(f"Notification: Package {data.tracking_number} was deleted")
        else:
            print(f"Unknown action: {action} for package {data.tracking_number}")


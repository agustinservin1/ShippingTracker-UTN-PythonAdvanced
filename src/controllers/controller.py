from src.models.db_models import Shipping, State, session, ShippingState
from src.utils.decorators import validate_address, calculate_costs
from src.utils.observers import StateObserver
from typing import List, Union

class ShippingController:
    
    def __init__(self) -> None:
        self.observers: List[StateObserver] = [StateObserver()]

    def register_observer(self, observer:StateObserver) -> None:
        self.observers.append(observer)

    def notify_observers(self, action: str, data: Union[Shipping,State]) -> None:
        for observer in self.observers:
            observer.update(action, data)
    def get_package(self, tracking_number: str):
        try:
            package = session.query(Shipping).filter_by(tracking_number=tracking_number).first()
            if not package:
                return "Error: Package not found"
            return str(package)
        except Exception as e:
            return f"Error querying package: {str(e)}"

    def get_package_states(self, tracking_number: str):
        try:
            package = session.query(Shipping).filter_by(tracking_number=tracking_number).first()
            if not package:
                return "Error: Package not found"
            return [str(state) for state in package.states]
        except Exception as e:
            return f"Error querying states: {str(e)}"

    def get_all_packages(self):
        try:
            packages = session.query(Shipping).all()
            return [str(package) for package in packages]
        except Exception as e:
            return f"Error querying packages: {str(e)}"

    @validate_address
    def create_package(self, tracking_number: str, sender_address: str, recipient_address: str) -> str:
        try:
            package = Shipping(
                tracking_number=tracking_number,
                sender_address=sender_address,
                recipient_address=recipient_address,
                current_state=ShippingState.CREATED 
            )
            session.add(package)
            session.commit()
            return f"Package created: {package}"
        except Exception as e:
            session.rollback()
            return f"Error creating package: {str(e)}"
    @calculate_costs
    def add_state(self, package_id: int, state: str, location: str, distance: int, weight: int):
        try:
            package = session.query(Shipping).get(package_id)
            if not package:
                return "Package not found."

            if state not in ShippingState.__members__:
                return "Invalid state."

            state_instance = State(
                shipping=package,
                state=ShippingState[state],
                location=location,
                distance = distance,
                weight = weight
                )
            
            session.add(state_instance)
            
            package.current_state = ShippingState[state]
            
            session.commit()

            return f"State added: {state_instance}"
        except Exception as e:
            session.rollback()
            return f"Error adding state: {str(e)}"


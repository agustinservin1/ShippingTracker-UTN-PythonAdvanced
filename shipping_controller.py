from model import Shipping, State, session, ShippingState

class ShippingController:
    def __init__(self):
        pass

    def create_package(self, tracking_number, sender_address, recipient_address):
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

    def add_state(self, package_id, state, location):
        try:
            package = session.query(Shipping).get(package_id)
            if not package:
                return "Package not found."

            if state not in ShippingState.__members__:
                return "Invalid state."

            state_instance = State(shipping=package, state=ShippingState[state], location=location)
            session.add(state_instance)
            package.current_state = ShippingState[state]
            session.commit()
            return f"State added: {state_instance}"
        except Exception as e:
            session.rollback()
            return f"Error adding state: {str(e)}"

# Example of how to use the enum states
controller = ShippingController()
print(controller.create_package("123ABC", "Sender Address", "Recipient Address"))
print(controller.add_state(1, "IN_TRANSIT", "Location A"))

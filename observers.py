class StateObserver:
    """Observer that reacts to changes in package states."""    
    def update(self, action, data):
        if action == "CREATE":
            print(f"Notification: Package {data.tracking_number} was created")
        elif action == "UPDATE":
            print(f"Notification: The state of package {data.shipping.tracking_number} changed to {data.state}")
        elif action == "DELETE":
            print(f"Notification: Package {data.tracking_number} was deleted")
        else:
            print(f"Unknown action: {action} for package {data.tracking_number}")


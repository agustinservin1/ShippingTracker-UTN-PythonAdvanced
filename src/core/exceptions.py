from fastapi import HTTPException

class ShippingException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class PackageNotFoundException(ShippingException):
    def __init__(self, tracking_number: str):
        super().__init__(
            status_code=404,
            detail=f"Package with tracking number {tracking_number} not found"
        )

class InvalidStateException(ShippingException):
    def __init__(self, state: str, valid_states: list):
        super().__init__(
            status_code=400,
            detail=f"Invalid state: {state}. Valid states are: {valid_states}"
        )
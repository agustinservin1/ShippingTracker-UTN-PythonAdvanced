from enum import Enum
from typing import List

class ShippingState(str, Enum):
    CREATED = "Created"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    RETURNED = "Returned"

    @classmethod
    def get_values(cls) -> List[str]:
        return [state.value for state in cls]

    @classmethod
    def is_valid(cls, state: str) -> bool:
        return state in cls.get_values()
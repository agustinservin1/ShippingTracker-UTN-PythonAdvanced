from typing import List,Union
from src.utils.observer.observers import Observer
from src.models import Shipping, State

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, action: str, data: Union[Shipping, State]) -> None:
        for observer in self._observers:
            observer.update(action, data)
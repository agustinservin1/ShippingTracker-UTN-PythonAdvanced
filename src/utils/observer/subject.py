from typing import List,Union
from src.utils.observer.observers import Observer
from src.models import Shipping, State

class ObservableEntity:
    def __init__(self):
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        if observer in self._observers:
          self._observers.remove(observer)

    def notify_observers(self, action: str, data: Union[Shipping, State]) -> None:
        for observer in self._observers:
             observer.update(action, data)

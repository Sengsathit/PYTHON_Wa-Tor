from abc import ABC, abstractmethod

class UISubject(ABC):
    """
    This abstract classs makes possible the notification between subject classes and UI (Obersver pattern)
    """

    def __init__(self):
        self._observers = []

    def attach_observer(self, observer):
        self._observers.append(observer)

    def detach_observer(self, observer):
        self._observers.remove(observer)
    
    def notify_chronon(self, value):
        for observer in self._observers:
            observer.refresh_chronon(value)

    def notify_stats(self, values):
        for observer in self._observers:
            observer.refresh_stats(values)

    def notify_fishes(self, fishes):
        for observer in self._observers:
            observer.refresh_fishes(fishes)

    def notify_end_simulation(self):
        for observer in self._observers:
            observer.stop_simulation()

class UIObserver(ABC):
    """
    This abstract classs makes possible the notification between subject classes and UI (Obersver pattern)
    """
     
    @abstractmethod
    def refresh_chronon(self, value):
        pass

    @abstractmethod
    def refresh_stats(self, values):
        pass

    @abstractmethod
    def refresh_fishes(self, fishes):
        pass

    @abstractmethod
    def stop_simulation(self):
        pass
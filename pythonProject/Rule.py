from abc import abstractmethod


class Rule:
    def __init__(self, name, event_type, points=1):
        super().__init__()
        self._name = name
        self._event_type = event_type
        self._points = points

    @abstractmethod
    def apply(self, events):
        pass

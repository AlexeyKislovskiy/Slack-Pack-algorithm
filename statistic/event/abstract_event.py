from abc import ABC, abstractmethod


class Event(ABC):
    """
    Abstract base class for all events.
    This class serves as a blueprint for different types of events that can occur.
    """

    @abstractmethod
    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.
        This method should be implemented by subclasses to return a string representing the event type.

        :return: The type of the event.
        """
        pass

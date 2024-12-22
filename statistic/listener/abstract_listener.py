from abc import ABC, abstractmethod

from statistic.event.abstract_event import Event


class StatisticListener(ABC):
    """
    An abstract base class for a statistic listener.
    This class defines the interface for objects that listen to events and process statistics accordingly.
    """

    @abstractmethod
    def handle(self, event: Event) -> None:
        """
        Process the given event.
        This method must be implemented by subclasses to define how an event should be handled.

        :param event: The event to be processed.
        """
        pass

    @abstractmethod
    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.
        This method must be implemented by subclasses to return the type of event the listener is interested in.

        :return: The type of event associated with this listener.
        """
        pass

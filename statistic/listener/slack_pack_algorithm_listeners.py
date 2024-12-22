from abc import abstractmethod
from statistic.event.slack_pack_algorithm_events import SlackPackAlgorithmAfterDetailPlacedEvent, \
    SlackPackAlgorithmBeforeLRPCutEvent, SlackPackAlgorithmAfterLRPCutEvent, SlackPackAlgorithmEndEvent
from statistic.listener.abstract_listener import StatisticListener


class AfterDetailPlacedListener(StatisticListener):
    """
    An abstract listener class for handling events after a detail has been placed during the Slack Pack algorithm.
    This class should be subclassed by classes that need to perform specific actions when a new detail is placed
    in the Slack Pack algorithm.
    """

    @abstractmethod
    def handle(self, event: SlackPackAlgorithmAfterDetailPlacedEvent) -> None:
        """
        Handle the event that occurs after a detail is placed.

        :param event: The event that occurs after a detail is placed.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return SlackPackAlgorithmAfterDetailPlacedEvent.EVENT_TYPE


class BeforeLRPCutListener(StatisticListener):
    """
    An abstract listener class for handling events before cutting a stripe from the LRP during the Slack Pack algorithm.
    This class should be subclassed by classes that need to perform specific actions before cutting a stripe
    from the LRP in the Slack Pack algorithm.
    """

    @abstractmethod
    def handle(self, event: SlackPackAlgorithmBeforeLRPCutEvent) -> None:
        """
        Handle the event that occurs before cutting a stripe from the LRP.

        :param event: The event that occurs before cutting a stripe from the LRP.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return SlackPackAlgorithmBeforeLRPCutEvent.EVENT_TYPE


class AfterLRPCutListener(StatisticListener):
    """
    An abstract listener class for handling events after cutting a stripe from the LRP during the Slack Pack algorithm.
    This class should be subclassed by classes that need to perform specific actions after cutting a stripe
    from the LRP in the Slack Pack algorithm.
    """

    @abstractmethod
    def handle(self, event: SlackPackAlgorithmAfterLRPCutEvent) -> None:
        """
        Handle the event that occurs after cutting a stripe from the LRP.

        :param event: The event that occurs after cutting a stripe from the LRP.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return SlackPackAlgorithmAfterLRPCutEvent.EVENT_TYPE


class AlgorithmEndListener(StatisticListener):
    """
    An abstract listener class for handling events that occurs at the end of the Slack Pack algorithm.
    This class should be subclassed by classes that need to perform specific actions at the end of the Slack Pack algorithm.
    """

    @abstractmethod
    def handle(self, event: SlackPackAlgorithmEndEvent) -> None:
        """
        Handle the event that occurs at the end of the Slack Pack algorithm.

        :param event: The event that occurs at the end of the Slack Pack algorithm.
        """
        pass

    def get_event_type(self) -> str:
        """
        Get the type of event associated with this listener.

        :return: The type of event associated with this listener.
        """
        return SlackPackAlgorithmEndEvent.EVENT_TYPE

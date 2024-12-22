from detail.detail import Detail
from statistic.event.abstract_event import Event


class SlackPackAlgorithmEvent(Event):
    EVENT_TYPE = 'Slack Pack algorithm event'

    """
    Base class for events that occur during the execution of the Slack Pack algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        n0 (int): The index of the first detail to be placed.
        max_placed (int): The maximum number of details to place.
        lrp (Detail): The Large Rectangular Piece (LRP).
        active_box (Detail): The current active box, or None if there is no current active box.
        active_box_first_detail_index (int): The index of the first detail in the current active box.
        is_active_box_horizontal (bool): Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        active_box_from (str): Type of the detail from which the current active box was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def __init__(self, gamma: float, n0: int, max_placed: int, lrp: Detail, active_box: Detail,
                 active_box_first_detail_index: int, is_active_box_horizontal: bool, last_placed_index: int,
                 endpoints_placed: int, active_box_from: str, detail: tuple[float, float],
                 placed_details: list[Detail]):
        """
        Initialize a SlackPackAlgorithmEvent object.

        :param gamma: The gamma parameter.
        :param n0: The index of the first detail to be placed.
        :param max_placed: The maximum number of details to place.
        :param lrp: The Large Rectangular Piece (LRP).
        :param active_box: The current active box, or None if there is no current active box.
        :param active_box_first_detail_index: The index of the first detail in the current active box.
        :param is_active_box_horizontal: Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        :param last_placed_index: The index of the last placed detail.
        :param endpoints_placed: The number of endpoints placed.
        :param active_box_from: The detail from which the current active box was formed.
        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: A list of placed details.
        """
        self.gamma = gamma
        self.n0 = n0
        self.max_placed = max_placed
        self.lrp = lrp
        self.active_box = active_box
        self.active_box_first_detail_index = active_box_first_detail_index
        self.is_active_box_horizontal = is_active_box_horizontal
        self.last_placed_index = last_placed_index
        self.endpoints_placed = endpoints_placed
        self.active_box_from = active_box_from
        self.detail = detail
        self.placed_details = placed_details

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class SlackPackAlgorithmAfterDetailPlacedEvent(SlackPackAlgorithmEvent):
    EVENT_TYPE = 'Slack Pack algorithm after detail placed event'

    """
    Event that occurs after placing a new detail during the execution of the Slack Pack algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        n0 (int): The index of the first detail to be placed.
        max_placed (int): The maximum number of details to place.
        lrp (Detail): The Large Rectangular Piece (LRP).
        active_box (Detail): The current active box, or None if there is no current active box.
        active_box_first_detail_index (int): The index of the first detail in the current active box.
        is_active_box_horizontal (bool): Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        active_box_from (str): Type of the detail from which the current active box was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
        placed_detail (Detail): The new placed detail.
        normal_box (Detail): The normal box created after placing the detail.
        endpoint (Detail): The endpoint created after placing the detail.
    """

    def __init__(self, gamma: float, n0: int, max_placed: int, lrp: Detail, active_box: Detail,
                 active_box_first_detail_index: int, is_active_box_horizontal: bool, last_placed_index: int,
                 endpoints_placed: int, active_box_from: str, detail: tuple[float, float], placed_details: list[Detail],
                 placed_detail: Detail, normal_box: Detail, endpoint: Detail):
        """
        Initialize a SlackPackAlgorithmDetailPlacedEvent object.

        :param gamma: The gamma parameter.
        :param n0: The index of the first detail to be placed.
        :param max_placed: The maximum number of details to place.
        :param lrp: The Large Rectangular Piece (LRP).
        :param active_box: The current active box, or None if there is no current active box.
        :param active_box_first_detail_index: The index of the first detail in the current active box.
        :param is_active_box_horizontal: Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        :param last_placed_index: The index of the last placed detail.
        :param endpoints_placed: The number of endpoints placed.
        :param active_box_from: The detail from which the current active box was formed.
        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: A list of placed details.
        :param placed_detail: The new placed detail.
        :param normal_box: The normal box created after placing the detail.
        :param endpoint: The endpoint created after placing the detail.
        """
        super().__init__(gamma, n0, max_placed, lrp, active_box, active_box_first_detail_index, is_active_box_horizontal,
                         last_placed_index, endpoints_placed, active_box_from, detail, placed_details)
        self.placed_detail = placed_detail
        self.normal_box = normal_box
        self.endpoint = endpoint

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class SlackPackAlgorithmBeforeLRPCutEvent(SlackPackAlgorithmEvent):
    EVENT_TYPE = 'Slack Pack algorithm before LRP cut event'

    """
    Event that occurs before cutting a stripe from the LRP during the execution of the Slack Pack algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        n0 (int): The index of the first detail to be placed.
        max_placed (int): The maximum number of details to place.
        lrp (Detail): The Large Rectangular Piece (LRP).
        active_box (Detail): The current active box, or None if there is no current active box.
        active_box_first_detail_index (int): The index of the first detail in the current active box.
        is_active_box_horizontal (bool): Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        active_box_from (str): Type of the detail from which the current active box was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class SlackPackAlgorithmAfterLRPCutEvent(SlackPackAlgorithmEvent):
    EVENT_TYPE = 'Slack Pack algorithm after LRP cut event'

    """
    Event that occurs after cutting a stripe from the LRP during the execution of the Slack Pack algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        n0 (int): The index of the first detail to be placed.
        max_placed (int): The maximum number of details to place.
        lrp (Detail): The Large Rectangular Piece (LRP).
        active_box (Detail): The current active box, or None if there is no current active box.
        active_box_first_detail_index (int): The index of the first detail in the current active box.
        is_active_box_horizontal (bool): Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        active_box_from (str): Type of the detail from which the current active box was formed.
        detail (tuple[float, float]): The current detail to be placed. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE


class SlackPackAlgorithmEndEvent(SlackPackAlgorithmEvent):
    EVENT_TYPE = 'Slack Pack algorithm end event'

    """
    Event that occurs at the end of the Slack Pack algorithm.

    Attributes:
        gamma (float): The gamma parameter.
        n0 (int): The index of the first detail to be placed.
        max_placed (int): The maximum number of details to place.
        lrp (Detail): The Large Rectangular Piece (LRP).
        active_box (Detail): The current active box, or None if there is no current active box.
        active_box_first_detail_index (int): The index of the first detail in the current active box.
        is_active_box_horizontal (bool): Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        active_box_from (str): Type of the detail from which the current active box was formed.
        detail (tuple[float, float]): The last placed detail. A tuple represents the width and height
            of the detail. The width here means the side on which the detail will be placed.
        placed_details (list[Detail]): A list of placed details.
    """

    def get_event_type(self) -> str:
        """
        Returns the type of the event as a string.

        :return: The type of the event.
        """
        return self.EVENT_TYPE

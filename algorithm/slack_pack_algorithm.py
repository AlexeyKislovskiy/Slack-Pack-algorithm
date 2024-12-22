from algorithm.abstract_algorithm import Algorithm, AlgorithmExecutionException
from detail.detail import Detail
from statistic.event.abstract_event import Event
from statistic.event.slack_pack_algorithm_events import SlackPackAlgorithmBeforeLRPCutEvent, SlackPackAlgorithmAfterLRPCutEvent, \
    SlackPackAlgorithmAfterDetailPlacedEvent, SlackPackAlgorithmEndEvent
from statistic.listener.abstract_listener import StatisticListener
from storage.abstract_box_storage import BoxStorage


class SlackPackAlgorithm(Algorithm):
    """
    SlackPackAlgorithm is a specific implementation of the Algorithm class for placing details on a sheet.
    This algorithm uses the gamma parameter to determine the placement strategy, including the cutting of new stripes
    and handling of normal boxes and endpoints.

    Attributes:
        gamma (float): The gamma parameter.
        n0 (int): The index of the first detail to be placed.
        max_placed (int): The maximum number of details to place.
        box_storage (BoxStorage): BoxStorage object for storing available boxes for placing details.
        statistic_listeners (list[StatisticListener]): List of statistic listeners to track during the execution.
        update_placed_details (bool): A flag indicating whether the list of placed details should be updated.
            If set to True, the list of placed details will be updated, allowing visualization of the layout
            and calculations based on the state of all placed details. Setting it to False can expedite the
            calculating process by bypassing the need for continuous updates of placed details.
        lrp (Detail): The Large Rectangular Piece (LRP).
        active_box (Detail): The current active box, or None if there is no current active box.
        active_box_first_detail_index (int): The index of the first detail in the current active box.
        is_active_box_horizontal (bool): Whether the active box is horizontal (the size along the x-axis is greater than
            along the y-axis).
        last_placed_index (int): The index of the last placed detail.
        endpoints_placed (int): The number of endpoints placed.
        active_box_from (str): Type of the detail from which the current active box was formed.
    """

    DETAIL_PREFIX = 'D'
    DETAIL_NAME = 'detail'
    NORMAL_BOX_PREFIX = 'B'
    NORMAL_BOX_TYPE_1_NAME = 'normal_box_1'
    NORMAL_BOX_TYPE_2_NAME = 'normal_box_2'
    ENDPOINT_PREFIX = 'E'
    ENDPOINT_TYPE_1_NAME = 'endpoint_1'
    ENDPOINT_TYPE_2_NAME = 'endpoint_2'
    LRP_PREFIX = 'LRP'
    LRP_NAME = 'lrp'

    def __init__(self, gamma: float, n0: int, max_placed: int, box_storage: BoxStorage,
                 statistic_listeners: list[StatisticListener] = None, update_placed_details: bool = True):
        """
        Initialize the SlackPackAlgorithm with the specified parameters.

        :param gamma: The gamma parameter.
        :param n0: The index of the first detail to be placed.
        :param max_placed: The maximum number of details to place.
        :param box_storage: BoxStorage object for storing available boxes for placing details.
        :param statistic_listeners: List of statistic listeners (optional).
        :param update_placed_details: A flag indicating whether the list of placed details should be updated.
            If set to True, the list of placed details will be updated, allowing visualization of the layout
            and calculations based on the state of all placed details. Setting it to False can expedite the
            calculating process by bypassing the need for continuous updates of placed details.
        """
        if statistic_listeners is None:
            statistic_listeners = []
        self.statistic_listeners = statistic_listeners
        self.gamma = gamma
        self.n0 = n0
        self.max_placed = max_placed
        self.box_storage = box_storage
        self.update_placed_details = update_placed_details
        self.lrp = None
        self.active_box = None
        self.active_box_first_detail_index = n0 - 1
        self.is_active_box_horizontal = False
        self.last_placed_index = n0 - 1
        self.endpoints_placed = 1
        self.active_box_from = None

    def place_next(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Place the next detail on the sheet using the Slack Pack algorithm.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        self._check_if_lrp_none(placed_details)
        self._check_active_box_size(detail)
        self._choose_active_box(detail, placed_details)
        self._place_detail_in_active_box(detail, placed_details)

    def _check_if_lrp_none(self, placed_details: list[Detail]) -> None:
        """
        Check if LRP is None and initialize it if necessary.
        If LRP is None, it initializes LRP as the first element of the placed_details list, which initially contains
        only an empty sheet. During other stages of the algorithm, situations where LRP is None should not occur.

        :param placed_details: List of details that have been placed so far.
        """
        if self.lrp is None:
            self.lrp = placed_details[0]

    def _check_active_box_size(self, detail: tuple[float, float]) -> None:
        """
        Check the size of the current active box.
        If the active box's size is insufficient to place a new detail with the required gap, the active box is set
        to None and the remaining part of it is added as a new endpoint.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        """
        if self.active_box is not None:
            required_gap = pow(1 / self.active_box_first_detail_index, self.gamma)
            total_length = detail[0] + required_gap
            if (self.is_active_box_horizontal and total_length > self.active_box.width) or \
                    (not self.is_active_box_horizontal and total_length > self.active_box.height):
                self.box_storage.add_box(self.active_box)
                self.active_box = None
                self.endpoints_placed += 1

    def _choose_active_box(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Choose a new active box for placing details if the current active box is None.
        If suitable boxes exist, the widest one is chosen; otherwise, a stripe is cut from LRP. If it's impossible
        to cut a stripe, an exception is raised.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        if self.active_box is None:
            self.active_box_first_detail_index = self.last_placed_index + 1
            max_box = self.box_storage.get_max_box()
            max_box_size = min(max_box.width, max_box.height) if max_box else -1
            required_gap = pow(1 / self.active_box_first_detail_index, self.gamma)
            total_length = detail[1] + required_gap
            if total_length <= max_box_size:
                self._choose_active_box_from_box()
            else:
                event = SlackPackAlgorithmBeforeLRPCutEvent(self.gamma, self.n0, self.max_placed, self.lrp, self.active_box,
                                                            self.active_box_first_detail_index,
                                                            self.is_active_box_horizontal,
                                                            self.last_placed_index, self.endpoints_placed,
                                                            self.active_box_from, detail, placed_details)
                self._notify_statistic_listeners(event)
                self._cut_new_strip(detail, placed_details)
                event = SlackPackAlgorithmAfterLRPCutEvent(self.gamma, self.n0, self.max_placed, self.lrp, self.active_box,
                                                           self.active_box_first_detail_index,
                                                           self.is_active_box_horizontal,
                                                           self.last_placed_index, self.endpoints_placed,
                                                           self.active_box_from, detail, placed_details)
                self._notify_statistic_listeners(event)

    def _choose_active_box_from_box(self) -> None:
        """
        Choose the widest available box as the new active box for placing details. Called only when a suitable box exists.
        """
        self.active_box = self.box_storage.pop_max_box()
        self.active_box_from = self.active_box.detail_type
        self.is_active_box_horizontal = self.active_box.width >= self.active_box.height

    def _cut_new_strip(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Cut a new stripe from LRP if no suitable box exists.
        Called only when there is no suitable box for placing a new detail. Raises an exception if it's impossible
        to cut a stripe.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        self.active_box_from = self.lrp.detail_type
        required_gap = pow(1 / (self.last_placed_index + 1), self.gamma)
        if detail[1] + required_gap > max(self.lrp.width, self.lrp.height) or \
                detail[0] + required_gap > min(self.lrp.width, self.lrp.height):
            raise AlgorithmExecutionException("Unable to cut a new stripe, LRP is too small")
        if self.lrp.width <= self.lrp.height:
            self.is_active_box_horizontal = True
            active_box_bottom_left = self.lrp.bottom_left
            active_box_top_right = (self.lrp.top_right[0], self.lrp.bottom_left[1] + detail[1] + required_gap)
            new_lrp_bottom_left = (self.lrp.bottom_left[0], self.lrp.bottom_left[1] + detail[1] + required_gap)
            new_lrp_top_right = self.lrp.top_right
        else:
            self.is_active_box_horizontal = False
            active_box_bottom_left = (self.lrp.top_right[0] - detail[1] - required_gap, self.lrp.bottom_left[1])
            active_box_top_right = self.lrp.top_right
            new_lrp_bottom_left = self.lrp.bottom_left
            new_lrp_top_right = (self.lrp.top_right[0] - detail[1] - required_gap, self.lrp.top_right[1])
        active_box = Detail(active_box_bottom_left, active_box_top_right,
                            f'{self.ENDPOINT_PREFIX}{self.endpoints_placed}',
                            self.ENDPOINT_TYPE_1_NAME)
        new_lrp = Detail(new_lrp_bottom_left, new_lrp_top_right, self.LRP_PREFIX, self.LRP_NAME)
        if self.update_placed_details:
            placed_details.remove(self.lrp)
            placed_details.append(active_box)
            placed_details.append(new_lrp)
        self.active_box = active_box
        self.lrp = new_lrp

    def _place_detail_in_active_box(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Place a detail into the active box.
        Called only when the necessary active box has already been chosen and there is enough space in it to place
        the detail with the required gap.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        normal_box_type = self._get_normal_box_type()
        endpoint_type = self._get_endpoint_type()

        self.last_placed_index += 1
        if self.is_active_box_horizontal:
            placed_detail_bottom_left = self.active_box.bottom_left
            placed_detail_top_right = (
            self.active_box.bottom_left[0] + detail[0], self.active_box.bottom_left[1] + detail[1])
            normal_box_bottom_left = (self.active_box.bottom_left[0], self.active_box.bottom_left[1] + detail[1])
            normal_box_top_right = (self.active_box.bottom_left[0] + detail[0], self.active_box.top_right[1])
            endpoint_bottom_left = (self.active_box.bottom_left[0] + detail[0], self.active_box.bottom_left[1])
            endpoint_top_right = self.active_box.top_right
        else:
            placed_detail_bottom_left = (self.active_box.top_right[0] - detail[1], self.active_box.bottom_left[1])
            placed_detail_top_right = (self.active_box.top_right[0], self.active_box.bottom_left[1] + detail[0])
            normal_box_bottom_left = self.active_box.bottom_left
            normal_box_top_right = (
            self.active_box.top_right[0] - detail[1], self.active_box.bottom_left[1] + detail[0])
            endpoint_bottom_left = (self.active_box.bottom_left[0], self.active_box.bottom_left[1] + detail[0])
            endpoint_top_right = self.active_box.top_right
        placed_detail = Detail(placed_detail_bottom_left, placed_detail_top_right,
                               f'{self.DETAIL_PREFIX}{self.last_placed_index}', self.DETAIL_NAME)
        normal_box = Detail(normal_box_bottom_left, normal_box_top_right,
                            f'{self.NORMAL_BOX_PREFIX}{self.last_placed_index}', normal_box_type)
        endpoint = Detail(endpoint_bottom_left, endpoint_top_right,
                          f'{self.ENDPOINT_PREFIX}{self.endpoints_placed}', endpoint_type)
        if self.update_placed_details:
            placed_details.remove(self.active_box)
            placed_details.append(placed_detail)
            placed_details.append(normal_box)
            placed_details.append(endpoint)
        self.active_box = endpoint
        self.box_storage.add_box(normal_box)
        event = SlackPackAlgorithmAfterDetailPlacedEvent(self.gamma, self.n0, self.max_placed, self.lrp, self.active_box,
                                                         self.active_box_first_detail_index, self.is_active_box_horizontal,
                                                         self.last_placed_index, self.endpoints_placed,
                                                         self.active_box_from, detail, placed_details, placed_detail,
                                                         normal_box, endpoint)
        self._notify_statistic_listeners(event)
        if self.last_placed_index == self.n0 + self.max_placed - 1:
            event = SlackPackAlgorithmEndEvent(self.gamma, self.n0, self.max_placed, self.lrp, self.active_box,
                                               self.active_box_first_detail_index, self.is_active_box_horizontal,
                                               self.last_placed_index, self.endpoints_placed,
                                               self.active_box_from, detail, placed_details)
            self._notify_statistic_listeners(event)

    def _get_normal_box_type(self) -> str:
        """
        Determine the type of normal box obtained when cutting from the current active box.
        If the active box is stripe cut from LRP, the box will be of the first type; otherwise, it will be the second type.

        :return: The type of normal box that will result from cutting from the current active box.
        """
        if self.active_box_from == self.LRP_NAME:
            return self.NORMAL_BOX_TYPE_1_NAME
        else:
            return self.NORMAL_BOX_TYPE_2_NAME

    def _get_endpoint_type(self) -> str:
        """
        Determine the type of endpoint obtained when cutting from the current active box.
        If the active box is stripe cut from LRP or a type 1 endpoint, the endpoint will be of the first type;
        otherwise, it will be the second type.

        :return: The type of endpoint that will result from cutting from the current active box.
        """
        if self.active_box_from == self.LRP_NAME or self.active_box_from == self.ENDPOINT_TYPE_1_NAME:
            return self.ENDPOINT_TYPE_1_NAME
        else:
            return self.ENDPOINT_TYPE_2_NAME

    def _notify_statistic_listeners(self, event: Event) -> None:
        """
        Notify statistic listeners after event occurred.

        :param event: The event to be processed.
        """
        for statistic in self.statistic_listeners:
            if statistic.get_event_type() == event.get_event_type():
                statistic.handle(event)

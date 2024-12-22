import math
import time

from algorithm.slack_pack_algorithm import SlackPackAlgorithm
from statistic.event.slack_pack_algorithm_events import SlackPackAlgorithmAfterDetailPlacedEvent, \
    SlackPackAlgorithmBeforeLRPCutEvent, SlackPackAlgorithmEndEvent
from statistic.listener.slack_pack_algorithm_listeners import AfterDetailPlacedListener, BeforeLRPCutListener, \
    AlgorithmEndListener
from statistic.output import OutputHandler


class PrintEachN(AfterDetailPlacedListener):
    """
    A listener that prints a message when a detail with an index multiple of n is placed.
    This class handles events that occur after a detail is placed during the Slack Pack algorithm,
    and outputs a message when the index of the last placed detail is a multiple of n.

    Attributes:
        n (int): The interval for indices at which to print messages.
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, n: int, output_handler: OutputHandler):
        """
        Initialize a PrintEachN object.

        :param n: The interval for indices at which to print messages.
        :param output_handler: The handler used to output messages.
        """
        self.n = n
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmAfterDetailPlacedEvent) -> None:
        """
        Handle the event that occurs after a detail is placed.
        If the index of the last placed detail is a multiple of n, print a message
        indicating the detail has been placed.

        :param event: The event that occurs after a detail is placed.
        """
        if event.last_placed_index % self.n == 0:
            message = f'Placed detail with index {event.last_placed_index}'
            self.output_handler.write(message)


class PrintInfoAtEnd(AlgorithmEndListener):
    """
    A listener that prints a message at the end of the Slack Pack algorithm.

    Attributes:
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, output_handler: OutputHandler):
        """
        Initialize an PrintInfoAtEnd object.

        :param output_handler: The handler used to output messages.
        """
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmEndEvent) -> None:
        """
        Handle the event that occurs at the end of the Slack Pack algorithm.
        Output information about end of the algorithm.

        :param event: The event that occurs at the end of the Slack Pack algorithm.
        """
        message = f'Slack Pack algorithm with n0 = {event.n0} and gamma = {event.gamma} ended'
        self.output_handler.write(message)


class ExecutionTimeTracker(AfterDetailPlacedListener):
    """
    A listener that tracks and outputs the execution time of the Slack Pack algorithm.
    This class handles events that occur after a detail is placed during the Slack Pack algorithm,
    measuring both the total execution time and the execution time for each block of n details.

    Attributes:
        n (int): The number of details in each block for which to measure the execution time.
        start_time (float): The timestamp when the first detail is placed, indicating the start of the execution.
        current_block_num (int): The current block number being measured.
        current_block_start_time (float): The timestamp when the current block started.
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, n: int, output_handler: OutputHandler):
        """
        Initialize an ExecutionTimeTracker object.

        :param n: The number of details in each block for which to measure the execution time.
        :param output_handler: The handler used to output messages.
        """
        self.n = n
        self.start_time = None
        self.current_block_num = 1
        self.current_block_start_time = None
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmAfterDetailPlacedEvent) -> None:
        """
        Handle the event that occurs after a detail is placed.
        Measures and outputs the execution time for each block of n details and the total execution time.

        :param event: The event that occurs after a detail is placed.
        """
        if not self.start_time:
            self.start_time = time.time()
        if not self.current_block_start_time:
            self.current_block_start_time = time.time()
        if event.last_placed_index % self.n == 0:
            end_time = time.time()
            execution_time = end_time - self.current_block_start_time
            message = f'Execution time of block {self.current_block_num} of {self.n} details: {execution_time} seconds'
            self.output_handler.write(message)
            self.current_block_num += 1
            self.current_block_start_time = None
        if event.last_placed_index == event.n0 + event.max_placed - 1:
            end_time = time.time()
            execution_time = end_time - self.start_time
            message = f'Full execution time: {execution_time} seconds'
            self.output_handler.write(message)


class NormalBoxMaxRatioTracker(AfterDetailPlacedListener):
    """
    A listener that tracks and outputs information about the maximum ratio of min_size / max_size^gamma
    for normal boxes resulting from the Slack Pack algorithm.
    This class handles events that occur after a detail is placed and calculates the ratio for each resulting
    normal box. It tracks sequences of maximum values and outputs information about these sequences.

    Attributes:
        current_max (float): The current maximum ratio.
        current_start_index (int): The index at which the current maximum sequence starts.
        current_start_value (float): The value of the ratio at the start of the current maximum sequence.
        current_finish_index (int): The index at which the current maximum sequence ends.
        current_finish_value (float): The value of the ratio at the end of the current maximum sequence.
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, output_handler: OutputHandler):
        """
        Initialize a NormalBoxMaxRatioTracker object.

        :param output_handler: The handler used to output messages.
        """
        self.current_max = -math.inf
        self.current_start_index = None
        self.current_start_value = None
        self.current_finish_index = None
        self.current_finish_value = None
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmAfterDetailPlacedEvent) -> None:
        """
        Handle the event that occurs after a detail is placed.
        Calculate the ratio for the normal box created by placing the detail.
        Track sequences of maximum values and output information about these sequences.

        :param event: The event that occurs after a detail is placed.
        """
        min_size = min(event.normal_box.height, event.normal_box.width)
        max_size = max(event.normal_box.height, event.normal_box.width)
        value = min_size / pow(max_size, event.gamma)
        if value > self.current_max:
            self.current_max = value
            self.current_finish_index = event.last_placed_index
            self.current_finish_value = value
            if self.current_start_index is None:
                self.current_start_index = event.last_placed_index
                self.current_start_value = value
        elif self.current_start_index is not None:
            message = f'{self.current_start_index} - {self.current_finish_index}:' \
                      f' {self.current_start_value} - {self.current_finish_value}'
            self.output_handler.write(message)
            self.current_start_index = None


class NormalBoxFinalMaxRatioTracker(AfterDetailPlacedListener):
    """
    A listener that tracks and outputs information about the maximum ratio of min_size / max_size^gamma
    for normal boxes resulting from the Slack Pack algorithm.
    This class only outputs the final maximum value at the end of the Slack Pack algorithm.

    Attributes:
        current_max (float): The current maximum ratio.
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, output_handler: OutputHandler):
        """
        Initialize a NormalBoxFinalMaxRatioTracker object.

        :param output_handler: The handler used to output messages.
        """
        self.current_max = -math.inf
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmAfterDetailPlacedEvent) -> None:
        """
        Handle the event that occurs after a detail is placed.
        Calculate the ratio for the normal box created by placing the detail. At the end of the algorithm,
        output the maximum ratio.

        :param event: The event that occurs after a detail is placed.
        """
        min_size = min(event.normal_box.height, event.normal_box.width)
        max_size = max(event.normal_box.height, event.normal_box.width)
        value = min_size / pow(max_size, event.gamma)
        if value > self.current_max:
            self.current_max = value
        if event.last_placed_index == event.n0 + event.max_placed - 1:
            message = f'n0 = {event.n0}, gamma = {event.gamma}, max_ratio = {self.current_max}'
            self.output_handler.write(message)


class LrpOccupancyRatioTracker(BeforeLRPCutListener):
    """
    A listener that calculates and outputs the proportion of the total free space on a sheet
    occupied by the Large Rectangular Piece (LRP) before a new stripe is cut from it.

    This class works correctly only if the update_placed_details flag in the Slack Pack algorithm is set to True.

    Attributes:
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, output_handler: OutputHandler):
        """
        Initialize an LrpOccupancyRatioTracker object.

        :param output_handler: The handler used to output messages.
        """
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmBeforeLRPCutEvent) -> None:
        """
        Handle the event that occurs before a new stripe is cut from the LRP.
        Calculate the proportion of the total free space occupied by the LRP and output this information.

        Note:
            This method works correctly only if the update_placed_details flag in the Slack Pack algorithm is set to True.

        :param event: The event that occurs before a new stripe is cut from the LRP.
        """
        lrp_area = event.lrp.width * event.lrp.height
        free_area = sum(detail.width * detail.height for detail in event.placed_details if
                        detail.detail_type != SlackPackAlgorithm.DETAIL_NAME)
        lcp_ratio = lrp_area / free_area
        self.output_handler.write(f'Placed: {event.last_placed_index}, lrp: {lcp_ratio}')


class LrpOccupancyRatioHarmonicRectangleTracker(BeforeLRPCutListener):
    """
    A listener that calculates and outputs the proportion of the total free space on a sheet
    occupied by the Large Rectangular Piece (LRP) before a new stripe is cut from it.

    This class is optimized for use with the HarmonicRectangleDetailGenerator and operates correctly
    even if the update_placed_details flag in the Slack Pack algorithm is set to False.

    Attributes:
        output_handler (OutputHandler): The handler used to output messages.
    """

    def __init__(self, output_handler: OutputHandler):
        """
        Initialize an LrpOccupancyRatioHarmonicRectangleTracker object.

        :param output_handler: The handler used to output messages.
        """
        self.output_handler = output_handler

    def handle(self, event: SlackPackAlgorithmBeforeLRPCutEvent) -> None:
        """
        Handle the event that occurs before a new stripe is cut from the LRP.
        Calculate the proportion of the total free space occupied by the LRP and output this information.

        Note:
            This method is optimized for the HarmonicRectangleDetailGenerator and works even if
            the update_placed_details flag in the Slack Pack algorithm is set to False.

        :param event: The event that occurs before a new stripe is cut from the LRP.
        """
        lrp_area = event.lrp.width * event.lrp.height
        free_area = 1 / (event.last_placed_index + 1)
        lcp_ratio = lrp_area / free_area
        self.output_handler.write(f'Placed: {event.last_placed_index}, lrp: {lcp_ratio}')

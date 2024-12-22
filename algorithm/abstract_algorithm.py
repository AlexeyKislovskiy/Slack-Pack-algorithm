from abc import ABC, abstractmethod
from detail.detail import Detail


class Algorithm(ABC):
    """
    Abstract base class for algorithms used to place details on a sheet.
    This class defines the interface that all concrete algorithms must implement.
    """

    @abstractmethod
    def place_next(self, detail: tuple[float, float], placed_details: list[Detail]) -> None:
        """
        Place the next detail on the sheet.
        This method must be implemented by subclasses to define how a detail is placed
        on the sheet according to the specific algorithm.

        :param detail: The current detail to be placed. A tuple represents the width and height of the detail.
            The width here means the side on which the detail will be placed.
        :param placed_details: List of details that have been placed so far.
        """
        pass


class AlgorithmExecutionException(Exception):
    """
    Exception raised for errors that occur during the execution of an algorithm.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message='Error during algorithms execution'):
        """
        Initialize the exception with an error message.

        :param message: Explanation of the error.
        """
        self.message = message
        super().__init__(self.message)

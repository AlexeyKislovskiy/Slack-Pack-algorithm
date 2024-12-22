import math
from abc import ABC, abstractmethod


class DetailGenerator(ABC):
    """
    Abstract base class for detail generators. This class defines the interface for generating
    sequential detail and getting the base size of the sheet where these detail will be placed.
    """

    def __iter__(self):
        """
        Returns the iterator object itself.

        :return: Iterator object.
        """
        return self

    @abstractmethod
    def __next__(self) -> tuple[float, float]:
        """
        Abstract method to return the next detail. Should be implemented in subclasses.

        :return: A tuple representing the width and height of the next detail. The width here means the side
        on which the detail will be placed.
        """
        pass

    @abstractmethod
    def get_base_size(self) -> tuple[float, float]:
        """
        Abstract method to return the size of the base sheet. Should be implemented in subclasses.

        :return: A tuple representing the width and height of the base sheet.
        """
        pass


class HarmonicSquareDetailGenerator(DetailGenerator):
    """
    Generator for square detail with harmonically decreasing sides.
    """

    def __init__(self, n0: int):
        """
        Initialize a HarmonicSquareDetailGenerator object.

        :param n0: The starting denominator for the first detail.
        """
        self.n0 = n0
        self.denominator = n0

    def __next__(self) -> tuple[float, float]:
        """
        Generate the next square detail with harmonically decreasing sides.

        :return: A tuple representing the width and height of the next square detail.
        """
        detail = (1 / self.denominator, 1 / self.denominator)
        self.denominator += 1
        return detail

    def get_base_size(self) -> tuple[float, float]:
        """
        Compute the size of the base sheet for square detail.

        :return: A tuple representing the width and height of the base sheet.
        """
        base_size = pow(math.pi, 2) / 6
        for i in range(1, self.n0):
            base_size -= pow(1 / i, 2)
        base_size = math.sqrt(base_size)
        return base_size, base_size


class HarmonicRectangleDetailGenerator(DetailGenerator):
    """
    Generator for rectangular detail with harmonically decreasing sides.
    """

    def __init__(self, n0: int, is_width_smaller: bool):
        """
        Initialize a HarmonicRectangleDetailGenerator object.

        :param n0: The starting denominator for the first detail.
        :param is_width_smaller: Boolean indicating if the width is smaller than the height.
        """
        self.n0 = n0
        self.denominator = n0
        self.is_width_smaller = is_width_smaller

    def __next__(self) -> tuple[float, float]:
        """
        Generate the next rectangular detail with harmonically decreasing sides.

        :return: A tuple representing the width and height of the next rectangular detail.
        """
        if self.is_width_smaller:
            detail = (1 / (self.denominator + 1), 1 / self.denominator)
        else:
            detail = (1 / self.denominator, 1 / (self.denominator + 1))
        self.denominator += 1
        return detail

    def get_base_size(self) -> tuple[float, float]:
        """
        Compute the size of the base sheet for rectangular detail.

        :return: A tuple representing the width and height of the base sheet.
        """
        base_size = math.sqrt(1 / self.n0)
        return base_size, base_size

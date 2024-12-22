from functools import cmp_to_key

from sortedcontainers import SortedSet

from detail.detail import Detail
from storage.abstract_box_storage import BoxStorage


class InMemoryBoxStorage(BoxStorage):
    """
     A class representing an in-memory storage for storing boxes during the detail placement process.

     Attributes:
         boxes (SortedSet[Detail]): A sorted set to store boxes.
     """

    def __init__(self):
        """
        Initializes the InMemoryBoxStorage with an empty SortedSet for storing boxes.
        """
        self.boxes = SortedSet(key=cmp_to_key(self._detail_comparator))

    def add_box(self, detail: Detail) -> None:
        """
        Add a box to the in-memory storage.

        :param detail: A Detail object representing the box to be added to the storage.
        """
        self.boxes.add(detail)

    def get_max_box(self) -> Detail:
        """
        Retrieve the largest box from the in-memory storage without removing it.

        :return: The largest box.
        """
        return self.boxes[0] if len(self.boxes) > 0 else None

    def pop_max_box(self) -> Detail:
        """
        Retrieve and remove the largest box from the in-memory storage.

        :return: The largest box.
        """
        return self.boxes.pop(0) if len(self.boxes) > 0 else None

    @staticmethod
    def _detail_comparator(detail1: Detail, detail2: Detail) -> float:
        """
        Compares two details based on their minimum side length.

        :param detail1: The first detail for comparison.
        :param detail2: The second detail for comparison.
        :return: Positive if detail1 is larger, negative if detail2 is larger, 0 if equal.
        """
        return min(detail2.width, detail2.height) - min(detail1.width, detail1.height)

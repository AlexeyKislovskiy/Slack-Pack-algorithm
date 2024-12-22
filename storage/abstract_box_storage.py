from abc import ABC, abstractmethod

from detail.detail import Detail


class BoxStorage(ABC):
    """
    Abstract base class for storing boxes during the detail placement.
    """

    @abstractmethod
    def add_box(self, detail: Detail) -> None:
        """
        Add a box to the storage.

        :param detail: A Detail object representing the box to be added to the storage.
        """
        pass

    @abstractmethod
    def get_max_box(self) -> Detail:
        """
        Retrieve the largest box from the storage without removing it.

        :return: The largest box.
        """
        pass

    @abstractmethod
    def pop_max_box(self) -> Detail:
        """
        Retrieve and remove the largest box from the storage.

        :return: The largest box.
        """
        pass

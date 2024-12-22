from algorithm.abstract_algorithm import Algorithm
from detail.detail_generator import DetailGenerator
from detail.detail import Detail


class DetailPlacer:
    """
    Class to coordinate the placement of details using a specified detail generator and algorithm.

    Attributes:
        algorithm (Algorithm): The algorithm used to place details.
        detail_generator (DetailGenerator): The detail generator used to create details.
        base_detail (Detail): The initial detail serving as the base for placement.
        max_placed (int): The maximum number of details to place.
    """

    def __init__(self, algorithm: Algorithm, detail_generator: DetailGenerator, base_detail: Detail, max_placed: int):
        """
        Initialize the DetailPlacer.

        :param algorithm: The algorithm used to place details.
        :param detail_generator: The detail generator used to create details.
        :param base_detail: The initial detail serving as the base for placement.
        :param max_placed: The maximum number of details to place.
        """
        self.algorithm = algorithm
        self.detail_generator = detail_generator
        self.base_detail = base_detail
        self.max_placed = max_placed

    def run_algorithm(self) -> list[Detail]:
        """
        Places details using the specified algorithm and generator, and returns the list of placed details.

        This method coordinates the generation of details from the detail generator, places them using
        the specified algorithm, and stops once the maximum number of details has been placed.

        :return: List of placed details.
        """
        num_placed = 0
        placed_details = [self.base_detail]
        detail_iterator = iter(self.detail_generator)
        try:
            for detail in detail_iterator:
                if num_placed < self.max_placed:
                    self.algorithm.place_next(detail, placed_details)
                    num_placed += 1
                else:
                    break
        except Exception as e:
            print(f"An error occurred during algorithm execution: {e}")
        finally:
            return placed_details

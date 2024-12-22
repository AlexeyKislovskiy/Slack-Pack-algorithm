from abc import ABC, abstractmethod


class OutputHandler(ABC):
    """
    An abstract class to handle output operations.
    """

    @abstractmethod
    def write(self, message: str) -> None:
        """
        Writes the given message.

        :param message: The message to be written.
        """
        pass


class ConsoleOutputHandler(OutputHandler):
    """
    A class to handle output operations to the console.
    """

    def write(self, message: str) -> None:
        """
        Writes the given message to the console.

        :param message: The message to be written.
        """
        print(message)


class FileOutputHandler(OutputHandler):
    """
    A class to handle output operations to a file.
    Supports appending to or overwriting a file.

    Attributes:
        file_path (str): The path to the file for output operations.
        mode (str): The mode of file output ('append', 'overwrite').
        first_write (bool): A flag to track the first write operation when in 'overwrite' mode.
    """

    APPEND = 'append'
    OVERWRITE = 'overwrite'

    def __init__(self, file_path: str, mode: str = APPEND):
        """
        Initializes the FileOutputHandler.

        :param file_path: The path to the file for file output.
        :param mode: The mode of file output. Can be 'append' or 'overwrite'. Default is 'append'.
        """
        self.file_path = file_path
        self.mode = mode
        self.first_write = True

    def write(self, message: str) -> None:
        """
        Writes the given message to the file according to the output mode.

        :param message: The message to be written.
        :raises ValueError: If the mode is invalid.
        """
        if self.mode == self.APPEND:
            with open(self.file_path, 'a') as f:
                f.write(f'{message}\n')
        elif self.mode == self.OVERWRITE:
            if self.first_write:
                with open(self.file_path, 'w') as f:
                    f.write(f'{message}\n')
                self.first_write = False
            else:
                with open(self.file_path, 'a') as f:
                    f.write(f'{message}\n')
        else:
            raise ValueError(f"Invalid mode: {self.mode}")
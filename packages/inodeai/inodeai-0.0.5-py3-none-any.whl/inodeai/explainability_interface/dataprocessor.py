import abc
from typing import Any

class DataProcessor(abc.ABC):
    """
    Abstract base class for processing different types of data.
    """

    @abc.abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process the data and return the result.
        :param data: Input data to be processed.
        :return: Processed data.
        """
        pass


class TextProcessor(DataProcessor):
    """
    Processor for handling text data.
    """

    def process(self, data: str) -> str:
        """
        Process text data.
        :param data: Text input data.
        :return: Processed text data.
        """
        # Example implementation (modify as needed)
        return data.strip().lower()


class ImageProcessor(DataProcessor):
    """
    Processor for handling image data.
    """

    def process(self, data: Any) -> Any:
        """
        Process image data.
        :param data: Image input data.
        :return: Processed image data.
        """
        # Example placeholder implementation (modify as needed)
        # Process the image (e.g., resize, normalize)
        return data  # Modify with actual processing logic


class StructuredDataProcessor(DataProcessor):
    """
    Processor for handling structured data.
    """

    def process(self, data: Any) -> Any:
        """
        Process structured data.
        :param data: Structured input data (e.g., DataFrame, CSV).
        :return: Processed structured data.
        """
        # Example placeholder implementation (modify as needed)
        return data  # Modify with actual processing logic



    # ImageProcessor and StructuredDataProcessor usage will depend on specific data requirements

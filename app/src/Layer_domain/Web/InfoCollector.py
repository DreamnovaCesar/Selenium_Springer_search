from abc import ABC
from abc import abstractmethod

class InfoCollector(ABC):
    """Abstract class for collecting information from a website."""

    @abstractmethod
    def collect_info(self, subject: str, Pages_number : int):
        pass
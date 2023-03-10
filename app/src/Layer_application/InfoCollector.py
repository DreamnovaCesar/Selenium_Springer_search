from abc import ABC
from abc import abstractmethod

from ..Layer_domain.Decorators.Singleton import Singleton
from ..Layer_domain.Decorators.Timer import Timer

#@Singleton.singleton
class InfoCollector(ABC):
    """
    An abstract class for collecting information from a website.

    Methods:
    --------
    collect_info(subject: str, Pages_number: int):
        Abstract method that must be implemented by subclasses to collect information from a website.

    """

    @Timer.timer
    @abstractmethod
    def collect_info(self, subject: str, Pages_number : int):
        """
        Abstract method that must be implemented by subclasses to collect information from a website.

        Parameters:
        -----------
        subject: str
            A string representing the subject of the information to be collected.

        Pages_number: int
            An integer representing the number of pages to be crawled to collect the information.

        Returns:
        --------
        None
        """
        pass
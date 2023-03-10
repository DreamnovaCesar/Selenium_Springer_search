from .MenuOption import MenuOption
from ..Layer_application.SpringerInfoCollector import SpringerInfoCollector

class DownloadCollector(MenuOption):
    """
    A MenuOption class that allows the user to download random images of girls.

    Attributes:
    -----------
    Collector : DownloadGirlsRandom
        The Collector object used to download the images.
    
    Methods
    -------
    execute()
        Prompts the user to input a path to a number of folders and the Nnumber of images to download. 
    """

    def __init__(self, 
                 Collector : SpringerInfoCollector):

        """
        Constructs a new DownloadRandomly object.
        """
        
        self.Collector = Collector;

    def execute(self):
        """
        Executes the DownloadRandomly option by prompting the user for the number of folders and images to download,
        and then downloading the random images using the Collector object.
        """
        
        self.Subject = input('Subject: ');
        self.Pages = input('Number of pages: ');
        Collector = self.Collector();
        Collector.collect_info(self.Subject, self.Pages);
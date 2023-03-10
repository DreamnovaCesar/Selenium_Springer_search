__author__ = "Cesar Eduardo Munoz Chavez"
__license__ = "Feel free to copy"

# ? Import necessary modules
from .Layer_application import SpringerInfoCollector
from .Layer_presentation.DownloadCollector import DownloadCollector

from .Layer_presentation import Menu

# ? Define the options for the menu
options = {

    "Download spring data" : DownloadCollector(SpringerInfoCollector)

};

'''options = [
    DownloadCollector(SpringerInfoCollector)
]'''

# ? Create and display the menu
def main():
    menu = Menu(options);
    menu.display();

# ? If the script is being run directly, create and display the menu
if __name__ == "__main__":
    main();

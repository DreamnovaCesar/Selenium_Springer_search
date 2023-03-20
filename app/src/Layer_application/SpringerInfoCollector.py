import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

from .InfoCollector import InfoCollector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..utilities import Settings


class SpringerInfoCollector(InfoCollector):
    """
    Concrete class for collecting information from Springer website.

    Attributes
    ----------
    __Chrome_options : webdriver.ChromeOptions
        Chrome options for WebDriver.
    __Driver : webdriver.Chrome
        WebDriver instance.
    __Springer_link : str
        Link to Springer website.
    __Folder : str
        Path to folder where the data will be saved.
    __Columns_springer_info : list
        List of column names for the SpringerInfoCollector dataframe.
    __Columns_springer_info_lower : list
        List of lowercased column names for the SpringerInfoCollector dataframe.
    Dataframe_springer_info : pandas.DataFrame
        Dataframe for storing the scraped data.

    Methods
    -------
    collect_info(Subject: str) -> pandas.DataFrame:
        Collects information for a given search subject.

    """

    def __init__(self):

        # * Configures Chrome driver options to exclude logging and initializes Chrome driver
        self.__Chrome_options = webdriver.ChromeOptions()
        self.__Chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.__Driver = webdriver.Chrome(options = self.__Chrome_options)

        # * Sets the URL for Springer website and folder path for collected data
        self.__Springer_link = "https://link.springer.com/";
        self.__Folder = r'App\src\Data';
        self._Time_interval = 0.1;
        self._Implicitly = 10;
        self._Pages_implicitly = 0.5;

        # * Sets the columns for the collected data in uppercase and lowercase for comparison
        self.__Columns_springer_info = (
            "Href", "Title", "Subtitle", "Authors", "Publication_title", "Year", "DOI"
        );
        
        self.__Columns_springer_info_lower = [
            i.lower() for i in self.__Columns_springer_info
        ];

        # * Initializes an empty Pandas DataFrame to store collected data
        self.Dataframe_springer_info = pd.DataFrame(columns = self.__Columns_springer_info);

    # * Decorator for timing how long the collect_info method takes to execute
    def collect_info(self, Subject: str, Pages_number : int = 20) -> pd.DataFrame:
        """
        Collects information for a given search subject.

        Parameters
        ----------
        Subject : str
            The subject to search for.

        Returns
        -------
        pandas.DataFrame
            The dataframe containing the collected data.
        """

        # * Convertion string to integer
        Pages_number = int(Pages_number)

        # * Sets a value for the sleep time and navigates to the Springer website
        self.__Driver.get(self.__Springer_link);
        self.__Driver.implicitly_wait(self._Implicitly);

        # * Waits until the search box is present on the page
        Search_box = WebDriverWait(self.__Driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Settings._ID_QUERY_)));

        # * Enters the search term into the search box and clicks the search button
        Search_box.send_keys(Subject);
        time.sleep(self._Time_interval);
        Search_button = self.__Driver.find_element(By.XPATH, Settings._ID_SEARCH_);
        Search_button.click();

        # * Initializes an empty Pandas DataFrame to store collected data
        Dataframe_springer_info = pd.DataFrame(columns = self.__Columns_springer_info);

        # * Iterates over pages_number value search results and collects information
        for _ in range(Pages_number):
            
            # Waits for the search results to load
            self.__Driver.implicitly_wait(self._Time_interval);

            # Finds the list of search results and iterates over each publication
            Results_list = self.__Driver.find_element(By.CLASS_NAME, Settings._CONTENT_LIST_);
            Publications = Results_list.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_);
            None_ = 'None';

            for _, Publication in enumerate(Publications):
                
                Columns_values = [];

                # * Tries to extract the href links for the publication and appends to column_values
                try:
                    Links = Publication.find_elements(By.CLASS_NAME, self.__Columns_springer_info[1].lower())
                    
                    for link in Links:
                        print("{}: {}".format(self.__Columns_springer_info[0], link.get_attribute(self.__Columns_springer_info_lower[0])));
                        Link_href = link.get_attribute(self.__Columns_springer_info_lower[0].lower());
                        Columns_values.append(Link_href);

                except NoSuchElementException:
                    # * Appends empty string to column_values if the element is not found
                    Columns_values.append('');
                    print(None_);

                try:
                    Title = Publication.find_element(By.CLASS_NAME, 'title').text;
                    print("{}: {}".format(self.__Columns_springer_info[1], Title));
                    Columns_values.append(Title);

                except NoSuchElementException:
                    Columns_values.append('');
                    print(None_);
                    
                try:
                    Subtitle = Publication.find_element(By.CLASS_NAME, 'subtitle').text;
                    print("{}: {}".format(self.__Columns_springer_info[2], Subtitle));
                    Columns_values.append(Subtitle);

                except NoSuchElementException:
                    Columns_values.append('');
                    print(None_);

                try:
                    Authors = Publication.find_element(By.CLASS_NAME, 'authors').text;
                    print("{}: {}".format(self.__Columns_springer_info[3], Authors));
                    Columns_values.append(Authors);

                except NoSuchElementException:
                    Columns_values.append('');
                    print(None_);

                try:
                    Publication_title = Publication.find_element(By.CLASS_NAME, 'publication-title').text;
                    print("{}: {}".format(self.__Columns_springer_info[4], Publication_title));
                    Columns_values.append(Publication_title);

                except NoSuchElementException:
                    Columns_values.append('');
                    print(None_);

                try:
                    Year = Publication.find_element(By.CLASS_NAME, 'year').text;
                    print("{}: {}".format(self.__Columns_springer_info[5], Year));
                    Columns_values.append(Year);

                except NoSuchElementException:
                    Columns_values.append('');
                    print(None_);

                # * navigate to another website in the new ta
                self.__Driver.execute_script("window.open('');");

                # * switch to the new tab
                self.__Driver.switch_to.window(self.__Driver.window_handles[-1]);

                # * Navigate to another website in the new tab
                if(Link_href):
                    self.__Driver.get(Link_href);

                    # * Waiting time
                    self.__Driver.implicitly_wait(self._Pages_implicitly);
                    
                    # * Search for DOI information
                    try:

                        Table_info = self.__Driver.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_LIST_);
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_);

                        for Cell in Cells_info:
                            DOI_text = Cell.find_element(By.CLASS_NAME, Settings._DOI_TEXT_).text;

                            if(DOI_text == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_VALUE_).text;

                        print("{}: {}".format(self.__Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);

                    try:

                        Table_info = self.__Driver.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_LIST_UMB24_);
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_);

                        for Cell in Cells_info:
                            DOI_text = Cell.find_element(By.CLASS_NAME, Settings._DIGITAL_OBJECT_IDENTIFIER_).text;

                            if(DOI_text == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_VALUE_).text;

                        print("{}: {}".format(self.__Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('');
                        print(None_);
                    
                    New_row_to_add = dict(zip(self.__Columns_springer_info, Columns_values));
                    
                    # * Name CSV file and save it to the folder
                    Dataframe_springer_info = Dataframe_springer_info.append(pd.Series(New_row_to_add), ignore_index = True);
                    Dataframe_springer_info_name = "{}_info.csv".format(Subject);
                    Dataframe_springer_info_csv = os.path.join(self.__Folder, Dataframe_springer_info_name);
                    Dataframe_springer_info.to_csv(Dataframe_springer_info_csv, index = False);
                
                    #print(Dataframe_springer_info);

                    # * Interval times
                    time.sleep(self._Time_interval);

                    # * close the new tab
                    self.__Driver.close();

                    # * switch back to the original tab
                    self.__Driver.switch_to.window(self.__Driver.window_handles[0]);

            # * Interval times
            time.sleep(self._Time_interval);
            
            # * Button to change the current page to the new page
            Next_button = self.__Driver.find_element(By.CLASS_NAME, 
                                                     Settings._NEXT_CONTEST_LIST_);
            Next_button.click();

        # * Interval times
        time.sleep(self._Time_interval);

        # * Close Driver
        self.__Driver.quit();
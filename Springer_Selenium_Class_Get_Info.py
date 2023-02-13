
# ?
import os
import time
import string
import pandas as pd

import json

# ? An extensible library for opening URLs using a variety of protocols
import urllib.request

# ?
from selenium import webdriver
from selenium.webdriver.common.by import By

# ?
from functools import wraps

# ? Profile the memory usage of a Python program
from memory_profiler import memory_usage
from memory_profiler import profile

from abc import ABCMeta
from abc import abstractmethod

from Springer_Selenium_Class_Libraries import *
from Springer_Selenium_Class_Utilities import Utilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import Springer_Selenium_Settings

# ?
class GetInfo(Utilities):
    """Class for getting information about publications related to the subject the user wants on the Springer website

    Parameters
    ----------
    Springer_link : str
        The URL for the Springer website.
    Subject : str
        The subject to search for on the Springer website.

    Methods
    -------
    __repr__()
        Returns a string representation of the `GetInfo` class object.
    __str__()
        Returns a string description of the `GetInfo` class object.
    __del__()
        Destructor for the `GetInfo` class.
    data_dic()
        Returns a dictionary of the `GetInfo` class object's attributes.
    get_info_springer()
        Scrapes information about publications related to the subject the user wants from the Springer website
        and stores it in a pandas dataframe.

    Examples
    --------
    >>> 
    >>> 
    >>>
    """

    # * Initializing (Constructor)
    def __init__(self, **kwargs) -> None:
        
        """Initializes the `GetInfo` class object with the `Springer_link` and `Subject` attributes.

        Parameters
        ----------
        kwargs : dict
            Dictionary of arguments to initialize the `GetInfo` class object.
        """

        self.__Spinger_link = "https://link.springer.com/";
        self.__Subject = kwargs.get('Subject', None);
        self.__Folder_path = kwargs.get('FolderPath', None);

        # * chromedriver path
        #self.__Path_chrome_driver = r"chromedriver.exe"

    # * Class variables
    def __repr__(self) -> str:

        kwargs_info = '''{}, {}'''.format(  self.__Spinger_link, 
                                            self.__Subject)

        return kwargs_info

    # * Class description
    def __str__(self) -> str:
        return  f'''{self.__Spinger_link},
                    {self.__Subject}''';
    
    # * Deleting (Calling destructor)
    def __del__(self):
        print('Destructor called, GetInfo class destroyed.');

    # * Get data from a dic
    def data_dic(self) -> dict:
        """Returns a dictionary of the `GetInfo` class object's attributes.

        Returns
        -------
        dict
            Dictionary of the `GetInfo` class object's attributes.
        """

        return {'Link': str(self.__Spinger_link),
                'Subject': str(self.__Subject)
                };

    def handle_element(Function, Column_name, Columns_values):
        try:
            Result = Function()
            print("{}: {}".format(Column_name, Result))
            Columns_values.append(Result)

        except NoSuchElementException:
            Columns_values.append('None')
            print("None")

    # ? Scrapes information from the Springer website and stores it in a pandas dataframe.
    @profile
    @Utilities.timer_func
    def get_info_springer(self) -> None:
        """
        This function uses the Selenium WebDriver to automate the process of searching for 
        information about publications related to "Artificial intelligence" on the Springer website. 
        The information obtained includes the publication link, title, subtitle, authors, 
        publication title, year, and DOI. 

        The function first sets up a Chrome webdriver with certain experimental options and sets a sleep value to control
        the timing between actions. It then navigates to the Springer website and inputs the search query. 
        The results of the search are obtained and processed one by one, with the publication information being scraped
        and added to the dataframe.

        The function uses try-except blocks to handle possible exceptions that may occur when searching for elements on the page.
        If a certain piece of information cannot be found for a publication, the value for that column in the dataframe is set to 'None'.
        """

        Chrome_options = webdriver.ChromeOptions()
        Chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        Time_sleep_value = 0.2

        Driver = webdriver.Chrome(options = Chrome_options)
        Driver.get(self.__Spinger_link)

        # * Amount of time to wait (in seconds)
        Driver.implicitly_wait(Time_sleep_value)

        Search_box = Driver.find_element(By.XPATH, Springer_Selenium_Settings._ID_QUERY_)
        Search_box.send_keys(self.__Subject)

        # * Interval times
        time.sleep(Time_sleep_value)

        Search_button = Driver.find_element(By.XPATH, Springer_Selenium_Settings._ID_SEARCH_)
        Search_button.click()

        # * A list in Python that contains the names of columns for a dataframe.
        Columns_springer_info = ['Href', 'Title', 'Subtitle', 'Authors', 'Publication_title', 'Year', 'DOI']
        Columns_springer_info_lower = [i.lower() for i in Columns_springer_info]

        print(Columns_springer_info_lower)

        Dataframe_springer_info = pd.DataFrame(columns = Columns_springer_info)

        #print(Dataframe)

        for i in range(20):
            
            # * Waiting time
            Driver.implicitly_wait(Time_sleep_value)

            #results_list = driver.find_element(By.XPATH, "//*[@id='results-list']")
            results_list = Driver.find_element(By.CLASS_NAME, Springer_Selenium_Settings._CONTENT_LIST_)
            publications = results_list.find_elements(By.TAG_NAME, Springer_Selenium_Settings._TAG_NAME_LI_)
            None_ = 'None'

            for j, publication in enumerate(publications):
                
                Columns_values = []

                try:
                    Links = publication.find_elements(By.CLASS_NAME, Columns_springer_info[1].lower())
                    
                    for link in Links:
                        print("{}: {}".format(Columns_springer_info[0], link.get_attribute(Columns_springer_info_lower[0])));
                        Link_href = link.get_attribute(Columns_springer_info_lower[0].lower());
                        Columns_values.append(Link_href);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Title = publication.find_element(By.CLASS_NAME, 'title').text;
                    print("{}: {}".format(Columns_springer_info[1], Title));
                    Columns_values.append(Title);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);
                    
                try:
                    Subtitle = publication.find_element(By.CLASS_NAME, 'subtitle').text;
                    print("{}: {}".format(Columns_springer_info[2], Subtitle));
                    Columns_values.append(Subtitle);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Authors = publication.find_element(By.CLASS_NAME, 'authors').text;
                    print("{}: {}".format(Columns_springer_info[3], Authors));
                    Columns_values.append(Authors);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Publication_title = publication.find_element(By.CLASS_NAME, 'publication-title').text;
                    print("{}: {}".format(Columns_springer_info[4], Publication_title));
                    Columns_values.append(Publication_title);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Year = publication.find_element(By.CLASS_NAME, 'year').text;
                    print("{}: {}".format(Columns_springer_info[5], Year));
                    Columns_values.append(Year);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                # open a new tab
                Driver.execute_script("window.open('');")

                # switch to the new tab
                Driver.switch_to.window(Driver.window_handles[-1])

                # navigate to another website in the new tab
                if Link_href:
                    Driver.get(Link_href)

                    # * Waiting time
                    Driver.implicitly_wait(Time_sleep_value)
                    
                    try:

                        Table_info = Driver.find_element(By.CLASS_NAME, Springer_Selenium_Settings._BIBLIOGRAPHIC_INFO_LIST_)
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Springer_Selenium_Settings._TAG_NAME_LI_)

                        for Cell in Cells_info:
                            DOI_title = Cell.find_element(By.CLASS_NAME, Springer_Selenium_Settings._DOI_TEXT_).text

                            if(DOI_title == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Springer_Selenium_Settings._BIBLIOGRAPHIC_INFO_VALUE_).text

                        print("{}: {}".format(Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);

                    try:

                        Table_info = Driver.find_element(By.CLASS_NAME, Springer_Selenium_Settings._BIBLIOGRAPHIC_INFO_LIST_UMB24_)
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Springer_Selenium_Settings._TAG_NAME_LI_)

                        for Cell in Cells_info:
                            DOI_title = Cell.find_element(By.CLASS_NAME, Springer_Selenium_Settings._DIGITAL_OBJECT_IDENTIFIER_).text

                            if(DOI_title == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Springer_Selenium_Settings._BIBLIOGRAPHIC_INFO_VALUE_).text

                        print("{}: {}".format(Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);
                    
                    New_row_to_add = dict(zip(Columns_springer_info, Columns_values))

                    print(New_row_to_add)
                    
                    Dataframe_springer_info = Dataframe_springer_info.append(pd.Series(New_row_to_add), ignore_index = True)
                    Dataframe_springer_info.to_csv(self.__Folder_path, index = False)
                
                    print(Dataframe_springer_info)

                    # * Interval times
                    time.sleep(Time_sleep_value);

                    # close the new tab
                    Driver.close()

                    # switch back to the original tab
                    Driver.switch_to.window(Driver.window_handles[0])

            # * Interval times
            time.sleep(Time_sleep_value);

            Next_button = Driver.find_element(By.CLASS_NAME, Springer_Selenium_Settings._NEXT_CONTEST_LIST_)
            Next_button.click()

        # * Interval times
        time.sleep(Time_sleep_value);

        Driver.quit()
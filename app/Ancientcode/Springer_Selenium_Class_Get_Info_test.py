
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

# ?
import os
import time
import string
import pandas as pd

# ? 
import urllib.request

# ?
from selenium import webdriver
from selenium.webdriver.common.by import By

# ?
from functools import wraps

# ?
from memory_profiler import memory_usage
from memory_profiler import profile

# ? Profile the memory usage of a Python program
from memory_profiler import memory_usage
from memory_profiler import profile

from abc import ABCMeta
from abc import abstractmethod

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from ..Utilities.Settings import Settings

# ?
class SpringerInfoCollector(object):
    

    # * Initializing (Constructor)
    def __init__(self, **kwargs) -> None:
        
        """Initializes the `GetInfo` class object with the `Springer_link` and `Subject` attributes."""

        self.__Spinger_link = "https://link.springer.com/";
        self.__Subject = kwargs.get('Subject', None);
        self.__Folder_path = kwargs.get('FolderPath', None);

        # * chromedriver path
        #self.__Path_chrome_driver = r"chromedriver.exe"

    # ? Scrapes information from the Springer website and stores it in a pandas dataframe.

    def get_info_springer(self) -> None:
        

        Chrome_options = webdriver.ChromeOptions()
        Chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        Time_sleep_value = 0.2

        Driver = webdriver.Chrome(options = Chrome_options)
        Driver.get(self.__Spinger_link)

        # * Amount of time to wait (in seconds)
        Driver.implicitly_wait(Time_sleep_value)

        Search_box = Driver.find_element(By.XPATH, Settings._ID_QUERY_)
        Search_box.send_keys(self.__Subject)

        # * Interval times
        time.sleep(Time_sleep_value)

        Search_button = Driver.find_element(By.XPATH, Settings._ID_SEARCH_)
        Search_button.click()

        # * A list in Python that contains the names of columns for a dataframe.
        Columns_springer_info = ['Title', 'Subtitle', 'Authors', 'Publication_title', 'Year', 'DOI']
        Columns_springer_info_lower = [i.lower() for i in Columns_springer_info]

        print(Columns_springer_info_lower)

        Dataframe_springer_info = pd.DataFrame(columns = Columns_springer_info)

        #print(Dataframe)

        for i in range(20):
            
            # * Waiting time
            Driver.implicitly_wait(Time_sleep_value)

            #results_list = driver.find_element(By.XPATH, "//*[@id='results-list']")
            results_list = Driver.find_element(By.CLASS_NAME, Settings._CONTENT_LIST_)
            publications = results_list.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_)
            None_ = 'None'

            for j, publication in enumerate(publications):
                
                Columns_values = []

                self.handle_element(lambda: publication.find_elements(By.CLASS_NAME, Columns_springer_info_lower[1])[0].get_attribute('href'), 
                                                                        Columns_springer_info[1], Columns_values)

                self.handle_element(lambda: publication.find_element(By.CLASS_NAME, Columns_springer_info_lower[1]).text, 
                                                                        Columns_springer_info[1], Columns_values)

                self.handle_element(lambda: publication.find_element(By.CLASS_NAME, Columns_springer_info_lower[2]).text, 
                                                                        Columns_springer_info[2], Columns_values)

                self.handle_element(lambda: publication.find_element(By.CLASS_NAME, Columns_springer_info_lower[3]).text, 
                                                                        Columns_springer_info[3], Columns_values)
                
                self.handle_element(lambda: publication.find_element(By.CLASS_NAME, Columns_springer_info_lower[4]).text, 
                                                                        Columns_springer_info[4], Columns_values)

                self.handle_element(lambda: publication.find_element(By.CLASS_NAME, Columns_springer_info_lower[5]).text, 
                                                                        Columns_springer_info[5], Columns_values)

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

                        Table_info = Driver.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_LIST_)
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_)

                        for Cell in Cells_info:
                            DOI_title = Cell.find_element(By.CLASS_NAME, Settings._DOI_TEXT_).text

                            if(DOI_title == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_VALUE_).text

                        print("{}: {}".format(Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);

                    try:

                        Table_info = Driver.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_LIST_UMB24_)
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_)

                        for Cell in Cells_info:
                            DOI_title = Cell.find_element(By.CLASS_NAME, Settings._DIGITAL_OBJECT_IDENTIFIER_).text

                            if(DOI_title == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_VALUE_).text

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

            Next_button = Driver.find_element(By.CLASS_NAME, Settings._NEXT_CONTEST_LIST_)
            Next_button.click()

        # * Interval times
        time.sleep(Time_sleep_value);

        Driver.quit()
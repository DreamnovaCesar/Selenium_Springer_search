import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

from ..Decorators.Timer import Timer
from ..Decorators.Singleton import Singleton

from .InfoCollector import InfoCollector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ...Utilities import Settings

@Singleton.singleton
class SpringerInfoCollector(InfoCollector):
    """Concrete class for collecting information from Springer website."""
    
    def __init__(self):

        self.__Chrome_options = webdriver.ChromeOptions()
        self.__Chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.__Driver = webdriver.Chrome(options = self.__Chrome_options)

        self.__Springer_link = "https://link.springer.com/";
        self.__Folder = r'App\src\Data';

        self.__Columns_springer_info = [
            "Href", "Title", "Subtitle", "Authors", "Publication_title", "Year", "DOI"
        ];
        
        self.__Columns_springer_info_lower = [
            i.lower() for i in self.__Columns_springer_info
        ];

        self.Dataframe_springer_info = pd.DataFrame(columns = self.__Columns_springer_info);

    @Timer.timer
    def collect_info(self, Subject: str) -> pd.DataFrame:
        
        Chrome_options = webdriver.ChromeOptions()
        Chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        Time_sleep_value = 0.2
        self.__Driver.get(self.__Springer_link)
        self.__Driver.implicitly_wait(Time_sleep_value)

        Search_box = WebDriverWait(self.__Driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Settings._ID_QUERY_)))

        #Search_box = self.Driver.find_element(By.XPATH, Settings._ID_QUERY_)
        Search_box.send_keys(Subject)

        # * Interval times
        time.sleep(Time_sleep_value)

        Search_button = self.__Driver.find_element(By.XPATH, Settings._ID_SEARCH_)
        Search_button.click()

        Dataframe_springer_info = pd.DataFrame(columns = self.__Columns_springer_info)

        #print(Dataframe)

        for _ in range(20):
            
            # * Waiting time
            self.__Driver.implicitly_wait(Time_sleep_value)

            #results_list = driver.find_element(By.XPATH, "//*[@id='results-list']")
            Results_list = self.__Driver.find_element(By.CLASS_NAME, Settings._CONTENT_LIST_)
            Publications = Results_list.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_)
    
            None_ = 'None'

            for _, Publication in enumerate(Publications):
                
                Columns_values = []

                try:
                    Links = Publication.find_elements(By.CLASS_NAME, self.__Columns_springer_info[1].lower())
                    
                    for link in Links:
                        print("{}: {}".format(self.__Columns_springer_info[0], link.get_attribute(self.__Columns_springer_info_lower[0])));
                        Link_href = link.get_attribute(self.__Columns_springer_info_lower[0].lower());
                        Columns_values.append(Link_href);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Title = Publication.find_element(By.CLASS_NAME, 'title').text;
                    print("{}: {}".format(self.__Columns_springer_info[1], Title));
                    Columns_values.append(Title);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);
                    
                try:
                    Subtitle = Publication.find_element(By.CLASS_NAME, 'subtitle').text;
                    print("{}: {}".format(self.__Columns_springer_info[2], Subtitle));
                    Columns_values.append(Subtitle);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Authors = Publication.find_element(By.CLASS_NAME, 'authors').text;
                    print("{}: {}".format(self.__Columns_springer_info[3], Authors));
                    Columns_values.append(Authors);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Publication_title = Publication.find_element(By.CLASS_NAME, 'publication-title').text;
                    print("{}: {}".format(self.__Columns_springer_info[4], Publication_title));
                    Columns_values.append(Publication_title);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                try:
                    Year = Publication.find_element(By.CLASS_NAME, 'year').text;
                    print("{}: {}".format(self.__Columns_springer_info[5], Year));
                    Columns_values.append(Year);

                except NoSuchElementException:
                    Columns_values.append('')
                    print(None_);

                # open a new tab
                self.__Driver.execute_script("window.open('');")

                # switch to the new tab
                self.__Driver.switch_to.window(self.__Driver.window_handles[-1])

                # navigate to another website in the new tab
                if(Link_href):
                    self.__Driver.get(Link_href)

                    # * Waiting time
                    self.__Driver.implicitly_wait(Time_sleep_value)
                    
                    try:

                        Table_info = self.__Driver.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_LIST_)
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_)

                        for Cell in Cells_info:
                            DOI_text = Cell.find_element(By.CLASS_NAME, Settings._DOI_TEXT_).text

                            if(DOI_text == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_VALUE_).text

                        print("{}: {}".format(self.__Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);

                    try:

                        Table_info = self.__Driver.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_LIST_UMB24_)
                        Cells_info = Table_info.find_elements(By.TAG_NAME, Settings._TAG_NAME_LI_)

                        for Cell in Cells_info:
                            DOI_text = Cell.find_element(By.CLASS_NAME, Settings._DIGITAL_OBJECT_IDENTIFIER_).text

                            if(DOI_text == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, Settings._BIBLIOGRAPHIC_INFO_VALUE_).text

                        print("{}: {}".format(self.__Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);
                    
                    New_row_to_add = dict(zip(self.__Columns_springer_info, Columns_values))

                    print(New_row_to_add)
                    
                    Dataframe_springer_info = Dataframe_springer_info.append(pd.Series(New_row_to_add), ignore_index = True)
                    Dataframe_springer_info_name = "{}_info.csv".format(Subject)
                    Dataframe_springer_info_csv = os.path.join(self.__Folder, Dataframe_springer_info_name)
                    Dataframe_springer_info.to_csv(Dataframe_springer_info_csv, index = False)
                
                    print(Dataframe_springer_info)

                    # * Interval times
                    time.sleep(Time_sleep_value);

                    # close the new tab
                    self.__Driver.close()

                    # switch back to the original tab
                    self.__Driver.switch_to.window(self.__Driver.window_handles[0])

            # * Interval times
            time.sleep(Time_sleep_value);

            Next_button = self.__Driver.find_element(By.CLASS_NAME, Settings._NEXT_CONTEST_LIST_)
            Next_button.click()

        # * Interval times
        time.sleep(Time_sleep_value);

        self.__Driver.quit()
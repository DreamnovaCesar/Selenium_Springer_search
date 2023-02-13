from Springer_Selenium_Class_Libraries import *
from Springer_Selenium_Class_Utilities import Utilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from abc import ABCMeta
from abc import abstractmethod

# ?
class GetInfo(Utilities, ABCMeta):
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
        
        self.__Spinger_link = "https://link.springer.com/";
        self.__Subject = kwargs.get('Subject', None)

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

        return {'Link': str(self.__Spinger_link),
                'Subject': str(self.__Subject)
                };

    # ?
    @profile
    @Utilities.timer_func
    def get_info_springer(self) -> None:
        """
        Scrapes information from the Springer website and stores it in a pandas dataframe.

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

        # * Waiting time
        Driver.implicitly_wait(Time_sleep_value)

        Search_box = Driver.find_element(By.XPATH, "//*[@id='query']")
        Search_box.send_keys("Artificial intelligence")

        # * Interval times
        time.sleep(Time_sleep_value)

        Search_button = Driver.find_element(By.XPATH, "//*[@id='search']")
        Search_button.click()

        # *
        Columns_springer_info = ['Link', 'Title', 'Subtitle', 'Authors', 'Publication_title', 'Year', 'DOI']
        Dataframe_springer_info = pd.DataFrame(columns = Columns_springer_info)

        #print(Dataframe)

        for i in range(20):
            
            # * Waiting time
            Driver.implicitly_wait(Time_sleep_value)

            #results_list = driver.find_element(By.XPATH, "//*[@id='results-list']")
            results_list = Driver.find_element(By.CLASS_NAME, "content-item-list")
            publications = results_list.find_elements(By.TAG_NAME, "li")
            None_ = 'None'

            for j, publication in enumerate(publications):
                
                Columns_values = []

                try:
                    Links = publication.find_elements(By.CLASS_NAME, 'title');
                    
                    for link in Links:
                        print("{}: {}".format(Columns_springer_info[0], link.get_attribute('href')));
                        Link_href = link.get_attribute('href');
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

                        Table_info = Driver.find_element(By.CLASS_NAME, "c-bibliographic-information__list")
                        Cells_info = Table_info.find_elements(By.TAG_NAME, "li")

                        for Cell in Cells_info:
                            DOI_title = Cell.find_element(By.CLASS_NAME, "u-text-bold").text

                            if(DOI_title == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, "c-bibliographic-information__value").text

                        print("{}: {}".format(Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);

                    try:

                        Table_info = Driver.find_element(By.CLASS_NAME, "c-bibliographic-information__list u-mb-24")
                        Cells_info = Table_info.find_elements(By.TAG_NAME, "li")

                        for Cell in Cells_info:
                            DOI_title = Cell.find_element(By.CLASS_NAME, "Digital Object Identifier").text

                            if(DOI_title == 'DOI'):
                                DOI = Cell.find_element(By.CLASS_NAME, "c-bibliographic-information__value").text

                        print("{}: {}".format(Columns_springer_info[6], DOI));
                        Columns_values.append(DOI);

                    except NoSuchElementException:
                        Columns_values.append('')
                        print(None_);
                    
                    New_row_to_add = dict(zip(Columns_springer_info, Columns_values))

                    print(New_row_to_add)
                    
                    Dataframe = Dataframe.append(pd.Series(New_row_to_add), ignore_index = True)
                    Dataframe.to_csv(r'D:\Test\Data.csv', index = False)
                
                    print(Dataframe)

                    # * Interval times
                    time.sleep(Time_sleep_value);

                    # close the new tab
                    Driver.close()

                    # switch back to the original tab
                    Driver.switch_to.window(Driver.window_handles[0])

            # * Interval times
            time.sleep(Time_sleep_value);

            Next_button = Driver.find_element(By.CLASS_NAME, 'next')
            Next_button.click()

        # * Interval times
        time.sleep(Time_sleep_value);

        Driver.quit()
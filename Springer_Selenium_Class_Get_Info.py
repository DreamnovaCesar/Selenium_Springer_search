from Springer_Selenium_Class_Libraries import *
from Springer_Selenium_Class_Utilities import Utilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from abc import ABCMeta
from abc import abstractmethod

# ?
class GetInfo(Utilities, ABCMeta):

    def __init__(self, **kwargs) -> None:
        pass
        # * chromedriver path
        #self.__Path_chrome_driver = r"chromedriver.exe"

    def __repr__(self):

        kwargs_info = "{}, {}".format()

        return kwargs_info

    def __str__(self):
        pass
    
    @profile
    @Utilities.timer_func
    def get_info_springer(self) -> None:

        
        Chrome_options = webdriver.ChromeOptions()
        Chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        Time_sleep_value = 0.2

        Driver = webdriver.Chrome(options = Chrome_options)
        Driver.get("https://link.springer.com/")

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
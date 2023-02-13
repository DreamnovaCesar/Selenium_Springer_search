from Springer_Selenium_Class_Libraries import *
from Springer_Selenium_Class_menu import *
from Springer_Selenium_Class_Get_Info import GetInfo
def main():  
    # *
    #config = Menu()
    #config.menu()

    AI = GetInfo()
    AI.get_info_springer()

if __name__ == "__main__":
    main()
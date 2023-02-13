
from Springer_Selenium_Class_Libraries import wraps
from Springer_Selenium_Class_Libraries import time

# ?
class Utilities(object):

    # ? Get the execution time of each function
    @staticmethod  
    def timer_func(func):  
        @wraps(func)  
        def wrapper(self, *args, **kwargs):  

            # * Obtain the executed time of the function

            Asterisk = 60;

            t1 = time.time();
            result = func(self, *args, **kwargs);
            t2 = time.time();

            print("\n");
            print("*" * Asterisk);
            print('Function {} executed in {:.4f}'.format(func.__name__, t2 - t1));
            print("*" * Asterisk);
            print("\n");

            return result
        return wrapper
import time
from functools import wraps

class Timer(object):
    """A decorator to measure the execution time of a function."""
    
    @staticmethod  
    def timer(func):
        """
        Decorator function that measures the execution time of a function.

        Parameters:
        -----------
        func : function
            The function to be timed.

        Returns:
        --------
        wrapper : function
            A function that executes the input function and prints the execution time.
        """
        @wraps(func)  
        def wrapper(*args, **kwargs):
            start_time = time.time();
            result = func(*args, **kwargs);
            end_time = time.time();
            print("\n");
            print("*" * 60);
            print('Function {} executed in {:.4f}'.format(func.__name__, end_time - start_time));
            print("*" * 60);
            print("\n");
            return result
        return wrapper
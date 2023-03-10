from functools import wraps

class Logger(object):
    """A decorator to log the input function's arguments and return value."""
    
    @staticmethod
    def log(func):
        """
        Decorator function that logs the input function's arguments and return value.

        Parameters:
        -----------
        func : function
            The function to be logged.

        Returns:
        --------
        wrapper : function
            A function that logs the input function's arguments and return value.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Function {func.__name__} called with args {args} and kwargs {kwargs}.");
            result = func(*args, **kwargs);
            print(f"Function {func.__name__} returned {result}.");
            return result
        return wrapper
import time
from functools import wraps

class Retry(object):
    """A decorator to retry a function with a delay."""

    @staticmethod
    def retry_with_delay(max_retries = 3, delay = 1):
        """
        Decorator function that retries a function a certain number of times with a delay between retries.

        Parameters:
        -----------
        max_retries : int
            The maximum number of retries.
        delay : int
            The delay in seconds between retries.

        Returns:
        --------
        decorator : function
            A decorator function that applies the retry logic to the input function.
        """
        def decorator(func):
            @wraps(func) 
            def wrapper(*args, **kwargs):
                for _ in range(max_retries):
                    try:
                        result = func(*args, **kwargs);
                        return result
                    except Exception as e:
                        print(f"Error occurred: {e}. Retrying in {delay} seconds...");
                        time.sleep(delay);
                raise Exception("Function failed after 3 retries.")
            return wrapper
        return decorator
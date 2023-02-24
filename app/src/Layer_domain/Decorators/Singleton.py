from functools import wraps

class Singleton(object):
    """A decorator to create singleton instances of a class."""
    
    @staticmethod
    def singleton(cls):
        """
        Decorator function that ensures a class has only one instance.

        Parameters:
        -----------
        cls : class
            The class to be made a singleton.

        Returns:
        --------
        wrapper : function
            A function that ensures only one instance of the input class is created.
        """

        instance = None
        @wraps(cls) 
        def wrapper(*args, **kwargs):
            nonlocal instance
            if instance is None:
                instance = cls(*args, **kwargs)
            return instance
        return wrapper
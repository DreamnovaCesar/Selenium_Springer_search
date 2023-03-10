class MenuOption(object):
    """
    A base class for implementing menu options. Subclasses must implement the execute method.

    Attributes:
        None

    Methods:
        execute(): This method must be implemented by subclasses. It will be called when the user selects
                   the menu option.
    """
    
    def execute(self):
        """
        This method must be implemented by subclasses. It will be called when the user selects the menu option.
        """
        raise NotImplementedError
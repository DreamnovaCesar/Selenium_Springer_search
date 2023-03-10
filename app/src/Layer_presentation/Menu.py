
class Menu(object):
    """
    A class representing a menu for displaying options and executing user-selected actions.

    Attributes
    ----------
    Options : dict
        A dictionary where the keys are the names of the options and the values are MenuOption objects.

    Methods
    -------
    display():
        Displays the menu options and prompts the user to select one. Executes the corresponding action 
        for the selected option.
    """

    def __init__(self, Options):
        """
        Parameters
        ----------
        Options : dict
            A dictionary where the keys are the names of the options and the values are MenuOption objects.
        """

        self.Options = Options;

        # * list out keys and values separately
        self._Options_text = list(self.Options.keys());
        self._Options_values = list(self.Options.values());

    def display(self):

        asterisk = 60;
        print("\n");
        print("*" * asterisk);
        print('What do you want to do:');
        print("*" * asterisk);
        print('\n');

        for i, option in enumerate(self._Options_text):
            print(f'{i + 1}: {option}');

        print('\n');
        print("*" * asterisk);

        while True:
            """
            Displays the menu options and prompts the user to select one. Executes the corresponding action 
            for the selected option.
            """
            
            print('\n');
            choice = input('Option: ');

            try:
                choice = int(choice);
            except ValueError:
                continue;

            if(choice < 1 or choice > len(self._Options_values)):
                continue;

            self._Options_values[choice - 1].execute();
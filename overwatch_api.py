import json
import datetime


class OverwatchAPI:
    """
    A class to retrieve menus and menu presets from the API data structure,
     using a reference file so stat options can be displayed before the user
     ever adds a player profile of their own. (See _get_reference_data method).

    The dictionary returned by the API is five levels deep, so you need a lot
     of keys to get a look at what you want:
     - 'mode': set by user toggle, either 'quickPlayStats' or 'competitiveStats'
     - 'key2': always set to 'careerStats' for our purposes
     - 'hero': set to 'allHeroes' by default but can change to a single hero's
       name should the user select only that hero
     - 'option': set by the option the user selects from the dropdown menu,
       such as 'average'.
     - 'stat': set by the stat the user selects in the stat listbox,
       such as 'eliminationsAvgPer10Min'.
    """

    def __init__(self, main_program):
        """
        Initializes API dictionary keys and the reference profile data used
         to fetch stat options.
        A default list of menu options is manually created because there are
         some options in the API that we don't want, and it's easier this way.
        """
        self.owh = main_program.owh

        # Reference API data structure from which to pull keys.
        self.ref_file = "save_files/reference_data.json"
        self.data_ref = self._get_reference_data()

        # Keys used to read the API data from highest to lowest dict level.
        # Defaults are just examples.
        self.mode = 'quickPlayStats'
        self.key2 = 'careerStats'  # Should never change.
        self.hero = 'allHeroes'
        self.option = 'average'
        self.stat = 'eliminationsAvgPer10Min'

        # The possible presets to be shown in the GUI dropdown menu.
        # A reference is created because the presets may change.
        self.menu_options_ref = [
            'assists', 'average', 'best', 'combat', 'heroSpecific',
            'game', 'matchAwards', 'miscellaneous']
        self.menu_options = self.menu_options_ref[:]

    def _get_reference_data(self):
        """
        Returns the API data for a player with over 40,000 games played.
        Ideally the program would simply not load available stats until the
         user adds a profile and show only the stat keys that all of the loaded
         profiles have in common, but that's a whole lot more complicated.
        Instead we'll work with a reference. It's simpler but it does have
         the downside of taking up more space and becoming out of date.
        A player with high play time on all heroes was selected to ensure
         the data file would include all available keys.
         (TODO: Check if that's actually necessary.)
        """
        with open(self.ref_file, 'r') as f:
            return json.load(f)

    def get_new_stat_menu_presets(self, heroes):
        """
        Returns menu options based on the number of heroes provided.

        - 0 heroes: Menu is empty.
        - 1 hero: Menu includes all options.
        - 2+ heroes: Menu includes all options except 'heroSpecific'.

        :param list heroes: current list of selected heroes
        :return: list of menu options
        """
        menu_options = self.menu_options_ref[:]

        if len(heroes) == 0:
            self.hero = 'allHeroes'
            return ['']

        # If there's only one hero, set the hero key to that hero.
        elif len(heroes) == 1:
            self.hero = self.owh.get_api_name(heroes[0])
            return menu_options

        # If there are multiple heroes, set the hero key to 'allHeroes'.
        elif len(heroes) > 1:
            menu_options.remove('heroSpecific')
            self.hero = 'allHeroes'
            return menu_options

    def get_new_stat_menu(self, option):
        """
        Returns a list of stats paired to the provided menu option.

        Ex: If the option 'game' is provided, the method returns ['gamesLost',
        'gamesPlayed', 'gamesWon', 'timePlayed'].

        If the provided key is not in the active list of accepted menu
        options, the method returns False instead.

        The AttributeError exception handles the heroes that do not have an
        'assists' stat category.

        All menu options are retrieved from the reference file.

        :param str option: stat menu option e.g. 'average'
        :return: list of stats or False if option was invalid
        """
        if option not in self.menu_options_ref:
            return False

        self.option = option

        try:
            stats = self.data_ref \
                ['quickPlayStats'][self.key2][self.hero][option].keys()
        except AttributeError:
            pass
        else:
            return stats

    def get_stat(self, profile, hero):
        """Returns a stat for a given profile and current key selection."""

        try:

            # For reasons I can't understand, the if/except block doesn't
            # catch the TypeError that occurs if this key doesn't exist,
            # so I'm catching it with an if-statement instead.

            if profile[self.mode][self.key2][hero][self.option] is None:
                return 0
            stat = profile[self.mode][self.key2][hero][self.option][self.stat]

        except KeyError or TypeError:
            return 0

        else:
            if isinstance(stat, str):
                return self._converted_str(stat)
            return stat

    def _converted_str(self, stat):
        """
        Converts a percentage or time stat to an int or float type.

        :param str stat: a percentage or time string
        :return: percentage (int) or duration (int / float)
        """
        for c in stat:
            if c == '%':  # String represents a percentage
                return int(stat.split('%')[0])
            if c == ':':  # String represents a duration
                return self._convert_time(stat)

        print("Uh oh, it looks like we were passed a value we couldn't "
              "handle. That wasn't meant to happen!")

    def _convert_time(self, n, convert=None):
        """
        Converts a time string to seconds; or hours or minutes if specified.

        Method supports 'hh:mm:ss', 'mm:ss', and 'ss' time formats.

        :param str n: time
        :arg convert: optional: 'hours' or 'minutes'
        :returns: converted time
        """
        s = [1, 60, 3600]
        secs = sum(x * int(t) for x, t in zip(s, reversed(n.split(':'))))

        if convert == 'hours':
            return round(secs / 3600, 1)

        if convert == 'minutes':
            return round(secs / 360)

        return secs

    def get_playtime(self, profile, hero):
        """Returns the playtime for a given profile and hero."""
        try:
            time = profile[self.mode][self.key2][hero]['game']['timePlayed']
        except KeyError or TypeError:
            return 0
        else:
            if time:
                return self._convert_time(time, convert='hours')
            return 0

    def get_games_played(self, profile, hero):
        """Returns the games played for a given profile and hero."""
        try:
            played = profile[self.mode][self.key2][hero]['game']['gamesPlayed']
        except KeyError:
            return 0
        except TypeError:
            return 0
        else:
            return played

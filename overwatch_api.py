import json


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
        self.key2 = 'careerStats'         # Should never change.
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
         0 heroes: menu is empty.
         1 hero: menu includes all options.
         2+ heroes: menu includes all options except 'heroSpecific'.
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

    def get_new_stat_menu(self, key):
        """
        Returns a list of menu options corresponding to the provided key.
        Ex: 'game' -> ['gamesLost', 'gamesPlayed', 'gamesWon', 'timePlayed'].
        If the provided key is not in the active list of accepted menu options,
         the method returns False instead.
        The menu options are retrieved from the reference file.
        """
        if key in self.menu_options_ref:
            self.option = key
            return self.data_ref['quickPlayStats'][self.key2]\
                [self.hero][key].keys()
        else:
            return False

    def get_stat(self, profile, hero):
        """Returns a stat for a given profile and current key selection."""
        try:
            stat = profile[self.mode][self.key2][hero][self.option][self.stat]
        except KeyError:
            return 0
        except TypeError:
            return 0
        else:
            return self._convert_stat(stat)

    def _convert_stat(self, stat):
        """Convert a stat to an integer if it is a duration or percentage."""
        try:
            iter(stat)
        except TypeError:
            return stat

        for c in stat:
            if c == '%':
                return int(stat.split('%')[0])
            elif c == ':':
                return self._convert_time(stat)

        return stat

    def _convert_time(self, n):
        """Converts an 'hh:mm:ss' or 'mm:ss' time string to seconds."""
        s = [1, 60, 3600]
        return sum(x * int(t) for x, t in zip(s, reversed(n.split(':'))))

    def get_playtime(self, profile, hero):
        """Returns the playtime for a given profile and hero."""
        try:
            time = profile[self.mode][self.key2][hero]['game']['timePlayed']
        except KeyError:
            return 0
        except TypeError:
            return 0
        else:
            if time:
                return self._convert_time(time)
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

"""
This program builds charts that display a stat for any given number of
 players and heroes in the Overwatch video game.

It is comprised of several major classes described below:
 - OverwatchStatsManager: binds all of the other classes together
 - UserFiles: writes and reads user files
 - PlayerProfile: fetches profile data for an Overwatch player
 - OverwatchAPI: interfaces with the API data structure
 - OverwatchHeroes: returns information about Overwatch heroes
 - OverwatchGUI: handles GUI creation and most user input logic

The overall step-by-step program logic can be roughly summarized as follows:
 1. Retrieve players previously stored on file, if available
 2. Retrieve Overwatch heroes categorized by role
 3. Retrieve stat keys categorized by type (determined by API data structure)
 4. Assemble the GUI and fill it with information retrieved in steps 1-3
 5. Allow the user to press a RUN button when all parameters for building
     charts have been satisfied (selected 1+ player, 1+ hero, and 1 stat)
 6. Retrieve all requested API data when the RUN button is pressed
 * TODO: Determine the best type of chart for the request
 * TODO: Structure and send the data to get drawn
 * TODO: (Optional) Something to do with saving charts to file?
"""
from overwatch_gui import OverwatchGUI
from player_files import UserFiles, PlayerProfile
from overwatch_heroes import OverwatchHeroes
from overwatch_api import OverwatchAPI
from overwatch_draw import OverwatchDraw
import json


class OverwatchStatsManager:
    """Name in progress."""

    def __init__(self):
        """Initialize all the classes we need."""

        self.files = UserFiles()
        self.owh = OverwatchHeroes()
        self.api = OverwatchAPI(self)
        self.gui = OverwatchGUI(self)
        self.draw = None

        self.profiles = {}

    def start_loop(self):
        """Get the program loop started."""
        self.gui.boot_gui()
        self.gui.fill_starting_content()
        self.gui.window.mainloop()

    def get_profile(self, tag, platform, region):
        """
        Attempts to retrieve a profile for a given player by first checking
        save files and, if this fails, making an API call.

        If data is found, saves the profile then checks privacy status.
        If profile is not private, stores data into memory and returns True.

        :param str tag: the player's battletag (e.g. Clovis-1467)
        :param str platform: the player's platform (pc, etc)
        :param str region: the player's region (us, eu, asia)

        :rtype: bool
        :returns: True if profile retrieval succeeded, False otherwise
        """

        def is_not_private(stats):
            """
            Checks privacy status of a profile.

            If the profile is not private, adds the profile to the active list
            and returns True.

            :param dict stats: dictionary of player stats from the API

            :rtype: bool
            :returns: True if profile is not private, or False
            """
            if stats['private']:
                self.gui.alert.print(f"Profile for > {tag} < is set to private!",
                                     color='yellow')
                return False
            else:
                self.profiles[tag] = stats
                return True

        # Create PlayerProfile object and retrieve data on file, if any.
        profile = PlayerProfile(tag, platform, region)
        data = profile.get_data_from_file()

        # If data was found on file: Check privacy status.
        if data is not False:
            self.gui.alert.print(f"Found data for {tag} on file.", color='cyan')
            return is_not_private(data)

        # If data was not found: Attempt to get it from https://ow-api.com.
        self.gui.alert.print(f"Attempting API call for {tag}", style='waiting')
        data_api = profile.get_data_from_api()

        # If API call succeeded: Write data to file, then check privacy status.
        if data_api.status_code == 200:
            data = data_api.json()
            self.files.save_profile(tag, data)
            self.gui.alert.print("Success", style='success')
            return is_not_private(data)

        # If API call failed: We can't go any further.
        self.gui.alert.print(data_api.status_code, style='api_fail')
        return False

    def cmd_save_profiles(self):
        """TODO: Do I, though?"""
        # self.owp.

    def cmd_run_stats(self):
        """TODO: Build this method."""

        # Disable the RUN button to prevent spam.
        self.gui.run.disable()
        self.gui.alert.print("Building charts...")

        # Get the selected stat.
        index = self.gui.panel_stat.box.curselection()
        self.api.stat = self.gui.panel_stat.box.get(index)

        self.draw = OverwatchDraw(self.get_table(), self.api.stat)
        self.draw.bar_group()
        self.gui.run.enable()

    def get_table(self):
        """
        Creates a table based on the requested stats in the GUI by cycling
        through each requested profile and hero, then filling lists of equal
        length that correspond to a table column:

        - Players
        - Heroes
        - Colors (associated with the heroes)
        - Games Played
        - 'X' (blank if under minimum playtime)
        - Value of the requested stat

        :return: Stat table where the keys are the column headers listed above
        and the values are their respective lists.
        """
        players, heroes, games, stats, colors, x = [], [], [], [], [], []

        # We should only care about stats for heroes with at least 3h played.
        min_time = 3 * 3_600

        # Create six lists of equal length, each corresponding to a category.
        for tag in self.profiles:
            for hero in self.gui.heroes:

                # Set variables for better readability.
                data = self.profiles[tag]
                api_hero = self.owh.get_api_name(hero)

                # Fetch games played and time played for the hero.
                played = self.api.get_games_played(data, api_hero)
                time = self.api.get_playtime(data, api_hero)

                # Fill the lists.
                players.append(tag.split('-')[0])
                heroes.append(hero)
                games.append(played)
                stats.append(self.api.get_stat(data, api_hero))
                colors.append(self.owh.get_color(hero))

                # Add an X mark to heroes with low time played.
                if time >= min_time:
                    x.append('')
                elif time < min_time:
                    x.append('X')

        # Pair each list to headers in a dictionary and return it.
        return {
            'Player': players,
            'Hero': heroes,
            'Color': colors,
            'Games Played': games,
            'X': x,
            self.api.stat: stats,
        }

    def cmd_quit(self):
        """TODO: Make this kill the whole program, not just the GUI."""
        self.gui.window.quit()


main = OverwatchStatsManager()
main.start_loop()

print(f"\n{main.gui.heroes}")
print(main.gui.players)
# print(main.api.option)
print(main.api.stat)
print(main.api.mode)
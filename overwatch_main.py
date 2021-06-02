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
        self.data = {}

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
            self.gui.alert.api_confirm("Success")
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

        self.get_stat_dict()
        self._determine_chart_type()
        # self.make_chart()
        self.gui.run.enable()

    def get_stat_dict(self):
        """TODO: Improve this."""
        heroes = []
        [heroes.append(self.owh.get_api_name(h)) for h in self.gui.heroes]

        dataset = {}
        for tag in self.profiles:

            hero_stats = {}
            for hero in heroes:
                # Only add hero stats if playtime is above minimum threshold.
                min_time = 3 * 3_600
                if self.api.get_playtime(self.profiles[tag], hero) >= min_time:
                    hero_stats[self.owh.get_proper_name(hero)] = \
                        self.api.get_stat(self.profiles[tag], hero)
                else:
                    hero_stats[self.owh.get_proper_name(hero)] = None

            if hero_stats:
                dataset[tag] = hero_stats

        print(json.dumps(dataset, indent=4))

    def _determine_chart_type(self):
        """TODO: Determine the type of chart we should build."""
        max_cols = 16
        if (num_heroes := len(self.gui.heroes)) > 3 and len(self.profiles) > 2:
            rows = int(num_heroes / max_cols) + 1
            cols = int(num_heroes / rows) + 1
            # fig = subplot type
        else:
            # fig = bargroup type
            pass

        print("This does nothing of relevance yet.")

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
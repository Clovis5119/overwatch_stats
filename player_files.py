import requests
import json
from pathlib import Path
from datetime import datetime


class UserFiles:
    """
    A class to retrieve Overwatch data from user files and save data to them.

    Directory structure is as follows:
        /path/OverwatchStatsManager.py
        /path/save_files/player_info.json
        /path/save_files/api_data/YY-MM-DD/data_Battletag.json

    Battle.net user information (battletag, platform, region) is saved to
     'player_info.json'. This is the info used to perform an API call and
     we store it to save time for users who re-launch the program.

    Overwatch profile data, containing loads of stats, is called from the API
     and stored in sub-folders inside the api_data folder. Inside those folders,
     the profile data is stored in a data_Battletag.json file.
    """
    def __init__(self):
        """Sets today's date and creates directories if they don't exist."""
        self.today = datetime.today().strftime('%Y-%m-%d')

        # Set directory paths.
        self.path_save_files = "save_files"
        self.file_players = f"{self.path_save_files}/player_info.json"
        self.path_profiles = f"{self.path_save_files}/api_data/{self.today}"

        # Create the directories if they don't exist.
        Path(self.path_save_files).mkdir(exist_ok=True)
        Path(self.path_profiles).mkdir(exist_ok=True)

    def get_saved_players(self):
        """Returns the data dump for a player profile if one exists."""
        try:
            with open(self.file_players, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return False

    def save_players(self, players):
        """Save the provided Battle.net user information to file."""
        with open(self.file_players, 'w') as f:
            json.dump(players, f, indent=4)

    def save_profile(self, tag, data):
        """Save the provided Overwatch profile data to file."""
        filename = f"{self.path_profiles}/data_{tag}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


class PlayerProfile(UserFiles):
    """
    This class represents a single player profile in Overwatch.
    It inherits from UserFiles for no good reason other than that this more
     conveniently allows them to share directory settings.

    Instantiate a PlayerProfile by passing a player's battletag, platform, and
     region information. You may then attempt to retrieve the profile data
     from an existing file or call the API for new data.
    """

    def __init__(self, tag, platform, region):
        """
        Initializes the profile with battletag, platform, and region info, then
         sets up the directory where profile data is stored and fetched.
        """
        super().__init__()
        # self.today = "2021-05-19"   # Uncomment to get stat for past days

        # Battle.net user information required to make an API call.
        self.tag = tag              # Also needed to pull file data.
        self.platform = platform
        self.region = region

        # Set directory path and create it if it doesn't exist.
        self.path_api_data = f"{self.path_save_files}/api_data/{self.today}"
        Path(self.path_api_data).mkdir(exist_ok=True)

        # Filename for the profile.
        self.filename = f"{self.path_api_data}/data_{self.tag}.json"

    def __repr__(self):
        return f"This is the player object for {self.tag}"

    def get_data_from_api(self):
        """
        Returns new profile data from ow-api.com. If the API call fails,
         var.status_code provides the error code. If successful, you may
         use var.json() to convert the data to a readable format.
        """
        url = ("https://ow-api.com/v1/stats/"
               f"{self.platform}/{self.region}/{self.tag}/complete")
        return requests.get(url)

    def get_data_from_file(self):
        """
        Returns profile data already saved on file. If the file is empty
         or doesn't exist, returns False. This only checks data for the
         current day. Manually set another date to override and get old data.
        """
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = False
            print(f"File not found for {self.tag}")
            return data
        else:
            if bool(data) is False:
                data = False
                print(f"Found a file for {self.tag}, but it was empty.")
            return data

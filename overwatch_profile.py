import requests
import json
from pathlib import Path
from datetime import datetime


class OverwatchProfile:
    """A class to represent user profiles in Overwatch."""

    def __init__(self, battletag='temp', platform='pc', region='us'):
        """Initializes the profile with an API call and storing the data in json format."""

        # Split the user's Battle.net tag for later use.
        self.tag = battletag
        self.plat = platform.lower().strip()
        self.reg = region.lower().strip()

        # Create the directory where user data will be stored.
        Path("user_data").mkdir(exist_ok=True)
        self.data = {}

        # Set the list of recognized platforms and regions.
        self.platforms = ['pc', 'etc']
        self.regions = ['us', 'eu', 'asia']

    def get_new_data(self):
        """Create new profile data by calling the API."""

        # Call and store the user data from ow-api.com in .json format.
        url = ("https://ow-api.com/v1/stats/"
               f"{self.plat}/{self.reg}/{self.tag}/complete")
        user_obj = requests.get(url)
        print(f"Status code:  {user_obj.status_code}")
        self.data = user_obj.json()

        # Write the data to a file. New file for new days to track changes.
        today = datetime.today().strftime('%Y-%m-%d')
        filepath = f"user_data/{today}"
        Path(filepath).mkdir(exist_ok=True)

        filename = f"{filepath}/data_{self.tag}.json"
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_file_data(self):
        """Pull profile data from existing files. Currently only works
        for a preset date. Goal is to allow choosing dates and comparison."""
        date = "2021-05-19"
        filename = f"user_data/{date}/data_{self.tag}.json"

        try:
            with open(filename, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {'file_not_found': True}
            pass

    def get_stat(self,
                 mode_key='quickPlayStats',
                 key1='careerStats',
                 hero_key='allHeroes',
                 key2='game',
                 key3='gamesWon'):
        """Returns the desired stat value for a given hero and type."""
        try:
            stat = self.data[mode_key][key1][hero_key][key2][key3]
        except KeyError:
            return None
        except TypeError:
            return None
        else:
            return stat

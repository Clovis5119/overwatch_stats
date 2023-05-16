class OverwatchHeroes:
    """
    This class holds a dictionary of Overwatch heroes keyed by their official
    name (no special characters, e.g. Torbjörn is Torbjorn).

    Paired to each hero name is a sub-dictionary of attributes such as the
    hero's role in the game, their associated color, and their name in the
    data structure created by the API (e.g. 'dVa' or 'wreckingBall').

    The class contains several methods for retrieving information about the
    heroes, like their color, role, or how many unique roles there are.
    """
    def __init__(self):
        """Initializes the dictionary of Overwatch heroes."""
        self.overwatch_heroes = {
            'Ana': {
                'API': 'ana',
                'Role': 'Support',
                'Color': '#6E89B1'
            },
            'Ashe': {
                'API': 'ashe',
                'Role': 'Damage',
                'Color': '#676869'
            },
            'Baptiste': {
                'API': 'baptiste',
                'Role': 'Support',
                'Color': '#57B2CB'
            },
            'Bastion': {
                'API': 'bastion',
                'Role': 'Damage',
                'Color': '#7B8E79'
            },
            'Brigitte': {
                'API': 'brigitte',
                'Role': 'Support',
                'Color': '#8B625D'
            },
            'Cassidy': {
                'API': 'cassidy',
                'Role': 'Damage',
                'Color': '#B05A5D'
            },
            'D.Va': {
                'API': 'dVa',
                'Role': 'Tank',
                'Color': '#ED93C7'
            },
            'Doomfist': {
                'API': 'doomfist',
                'Role': 'Damage',
                'Color': '#83534B'
            },
            'Echo': {
                'API': 'echo',
                'Role': 'Damage',
                'Color': '#9BCBF5'
            },
            'Genji': {
                'API': 'genji',
                'Role': 'Damage',
                'Color': '#96EE42'
            },
            'Hanzo': {
                'API': 'hanzo',
                'Role': 'Damage',
                'Color': '#B9B489'
            },
            'Junker Queen': {
                'API': 'junkerQueen',
                'Role': 'Tank',
                'Color': '#00c3ff'
            },
            'Junkrat': {
                'API': 'junkrat',
                'Role': 'Damage',
                'Color': '#E9BC51'
            },
            'Kiriko': {
                'API': 'kiriko',
                'Role': 'Support',
                'Color': '#00c3ff'
            },
            'Lifeweaver': {
                'API': 'lifeweaver',
                'Role': 'Support',
                'Color': '#00c3ff'
            },
            'Lucio': {
                'API': 'lucio',
                'Role': 'Support',
                'Color': '#84C951'
            },
            'Mei': {
                'API': 'mei',
                'Role': 'Damage',
                'Color': '#6CABEA'
            },
            'Mercy': {
                'API': 'mercy',
                'Role': 'Support',
                'Color': '#EBE9BB'
            },
            'Moira': {
                'API': 'moira',
                'Role': 'Support',
                'Color': '#9672E3'
            },
            'Orisa': {
                'API': 'orisa',
                'Role': 'Tank',
                'Color': '#458B42'
            },
            'Pharah': {
                'API': 'pharah',
                'Role': 'Damage',
                'Color': '#3C7BC6'
            },
            'Ramattra': {
                'API': 'ramattra',
                'Role': 'Tank',
                'Color': '#00c3ff'
            },
            'Reaper': {
                'API': 'reaper',
                'Role': 'Damage',
                'Color': '#7D3F51'
            },
            'Reinhardt': {
                'API': 'reinhardt',
                'Role': 'Tank',
                'Color': '#93A0A4'
            },
            'Roadhog': {
                'API': 'roadhog',
                'Role': 'Tank',
                'Color': '#B58C51'
            },
            'Sigma': {
                'API': 'sigma',
                'Role': 'Tank',
                'Color': '#93A0A4'
            },
            'Sojourn': {
                'API': 'sojourn',
                'Role': 'Damage',
                'Color': '#00c3ff'
            },
            'Soldier:76': {
                'API': 'soldier76',
                'Role': 'Damage',
                'Color': '#6A7794'
            },
            'Sombra': {
                'API': 'sombra',
                'Role': 'Damage',
                'Color': '#735AB9'
            },
            'Symmetra': {
                'API': 'symmetra',
                'Role': 'Damage',
                'Color': '#8FBDCE'
            },
            'Torbjorn': {
                'API': 'torbjorn',
                'Role': 'Damage',
                'Color': '#BF736D'
            },
            'Tracer': {
                'API': 'tracer',
                'Role': 'Damage',
                'Color': '#D89442'
            },
            'Widowmaker': {
                'API': 'widowmaker',
                'Role': 'Damage',
                'Color': '#9D6AA6'
            },
            'Winston': {
                'API': 'winston',
                'Role': 'Tank',
                'Color': '#A0A5BB'
            },
            'Wrecking Ball': {
                'API': 'wreckingBall',
                'Role': 'Tank',
                'Color': '#DB9242'
            },
            'Zarya': {
                'API': 'zarya',
                'Role': 'Tank',
                'Color': '#E97FB6'
            },
            'Zenyatta': {
                'API': 'zenyatta',
                'Role': 'Support',
                'Color': '#EDE581'
            },
        }

    def get_color(self, name):
        """Returns the color hex associated to an Overwatch hero."""
        try:
            return self.overwatch_heroes[name]['Color']
        except KeyError:
            return self.overwatch_heroes[self.get_proper_name(name)]['Color']

    def get_role_list(self):
        """Returns a list of all Overwatch hero roles, plus 'All'."""
        role_list = ['All']
        for hero in self.overwatch_heroes:
            role_list.append(self.get_role(hero))
        return sorted(set(role_list))

    def get_role(self, hero):
        """Returns the role of a given Overwatch hero."""
        return self.overwatch_heroes[hero]['Role']

    def get_heroes_by_role(self, role):
        """
        Returns a list of Overwatch heroes for a given role (All, Damage,
        Support, or Tank).

        :param str role: a hero role in Overwatch
        :returns: list of heroes matching that role
        """
        if role == 'All':
            return list(self.overwatch_heroes.keys())

        hero_list = []
        for hero in self.overwatch_heroes:
            if self.overwatch_heroes[hero]['Role'] == role:
                hero_list.append(hero)

        return hero_list

    def get_proper_name(self, name):
        """
        Attempts to convert an API-compatible hero name to its official
        version (Ex: dva --> D.Va).

        Returns False if it fails to match the input to a name.

        :param str name: API-compatible hero name
        :returns: official Overwatch hero name, or False

        """
        for hero in self.overwatch_heroes.keys():

            test_name = name.lower().strip()
            valid1 = hero.lower().strip()
            valid2 = self.overwatch_heroes[hero]['API'].lower().strip()

            if test_name == valid1 or test_name == valid2:
                return hero

        return False

    def get_api_name(self, hero):
        """
        Transforms an Overwatch hero name to be compatible with the API format.
        (Ex: D.Va --> dVa).

        **Note**: Special characters such as in 'Torbjörn' are not supported.

        :param str hero: official Overwatch hero name

        :returns: API-compatible hero name
        """
        return self.overwatch_heroes[hero]['API']


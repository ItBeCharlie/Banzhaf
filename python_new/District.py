class District:
    def __init__(self, name: str, id: int):
        """
        _id: Numerical Id used for storing the original input order

        _name: Name/Title of District

        _population: Population of District

        _population_proportion: Percentage of population living in this district compared to the county

        _votes_per_member: Calculated # of votes per member based off the Banzhaf Power Index

        _norm_bpi: The Normalized BPI score for this district in relation to the rest of the county

        _bpi_diff: _norm_bpi - _population_proportion
        """
        self._id = id
        self._name = name
        self._population = None
        self._population_proportion = None
        self._votes_per_member = None
        self._norm_bpi = None
        self._bpi_diff = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = value

    @property
    def population_proportion(self):
        return self._population_proportion

    @population_proportion.setter
    def population_proportion(self, value):
        self._population_proportion = value

    @property
    def votes_per_member(self):
        return self._votes_per_member

    @votes_per_member.setter
    def votes_per_member(self, value):
        self._votes_per_member = value

    @property
    def bpi_diff(self):
        return self._bpi_diff

    @bpi_diff.setter
    def bpi_diff(self, value):
        self._bpi_diff = value

    @property
    def norm_bpi(self):
        return self._norm_bpi

    @norm_bpi.setter
    def norm_bpi(self, value):
        self._norm_bpi = value

    # def compare_to(self, district, key='District') -> int:
    #     """
    #     ## Valid Keys:
    #     District |
    #     Population |
    #     Pop. Proportion |
    #     '# Votes / Member' |
    #     Normalized BPI Score |
    #     BPI Score |
    #     """
    #     return self.get_val(key) - district.get_val(key)

    def print_data(self):
        """
        Returns list of District Data formated to proper form in the following order:

        0. _name: str
        1. _population: str
        2. _population_proportion: f'{val:#.9g}'
        3. _votes_per_member: str
        4. _norm_bpi: f'{val:#.9g}'
        5. _bpi_diff: f'{val:#.9g}'
        """
        print_data = []
        print_data.append(f'{self._name}')
        print_data.append(f'{self._population}')
        print_data.append(f'{self._population_proportion:#.9g}')
        print_data.append(f'{self._votes_per_member}')
        print_data.append(f'{self._norm_bpi:#.9g}')
        print_data.append(f'{self._bpi_diff:#.9g}')
        return print_data

    def clone(self):
        """
        Returns a clone of the district with unique pointers for each variable
        """
        copy = District(self.name, self.id)
        copy.population = (self.population)
        copy.population_proportion = (self.population_proportion)
        copy.votes_per_member = (self.votes_per_member)
        copy.norm_bpi = (self.norm_bpi)
        copy.bpi_diff = (self.bpi_diff)
        return copy

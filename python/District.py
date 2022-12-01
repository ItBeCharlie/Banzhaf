from helper import *


class District:
    def __init__(self, number):
        self.number = number
        self.population = None
        self.population_proportion = None
        self.votes_per_member = None
        self.bpi = None
        self.norm_bpi = None

    def change_population(self, new_population):
        if is_int(new_population):
            self.population = int(new_population)
            return True
        return False

    def compare_to(self, district, key='District') -> int:
        """
        ## Valid Keys:
        District | 
        Population | 
        Pop. Proportion | 
        '# Votes / Member' | 
        Normalized BPI Score | 
        BPI Score | 
        """
        return self.get_val(key) - district.get_val(key)

    def get_val(self, key='District'):
        """
        ## Valid Keys:
        District
        Population
        Pop. Proportion
        '# Votes / Member'
        Normalized BPI Score
        BPI Score
        """
        if key == 'District':
            return self.number
        elif key == 'Population':
            return self.population
        elif key == 'Pop. Proportion':
            return self.population_proportion
        elif key == '# Votes / Member':
            return self.votes_per_member
        elif key == 'Normalized BPI Score':
            return self.norm_bpi
        elif key == 'BPI Score':
            return self.bpi
        return None

    def set_val(self, key, val):
        """
        ## Valid Keys:
        Population
        Pop. Proportion
        '# Votes / Member'
        Normalized BPI Score
        BPI Score
        """
        if key == 'Population':
            self.population = val
        elif key == 'Pop. Proportion':
            self.population_proportion = val
        elif key == '# Votes / Member':
            self.votes_per_member = val
        elif key == 'Normalized BPI Score':
            self.norm_bpi = val
        elif key == 'BPI Score':
            self.bpi = val

    def print_data(self, keys):
        print_data = {}
        for key in keys:
            val = self.get_val(key)
            if key in ['Pop. Proportion', 'BPI Score']:
                # val = format_percentage(val)
                val = f'{val:#.9g}'
            if key in ['Normalized BPI Score']:
                val = f'{val:#.9g}'
            if key in ['# Votes / Member']:
                val = round(val)
            print_data[key] = str(val)
        return print_data

    def clone(self):
        copy = District(self.number)
        copy.population = self.population
        copy.population_proportion = self.population_proportion
        copy.votes_per_member = self.votes_per_member
        copy.norm_bpi = self.norm_bpi
        copy.bpi = self.bpi
        return copy

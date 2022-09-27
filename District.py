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

    def get_val(self, key):
        match key:
            case 'District':
                return self.number
            case 'Population':
                return self.population
            case 'Pop. Proportion':
                return self.population_proportion
            case '# Votes / Member':
                return self.votes_per_member
            case 'Normalized BPI Score':
                return self.norm_bpi
            case 'BPI Score':
                return self.bpi
        return None

    def set_val(self, key, val):
        match key:
            case 'Population':
                self.population = val
            case 'Pop. Proportion':
                self.population_proportion = val
            case '# Votes / Member':
                self.votes_per_member = val
            case 'Normalized BPI Score':
                self.norm_bpi = val
            case 'BPI Score':
                self.bpi = val

    def print_data(self, keys):
        print_data = {}
        for key in keys:
            val = self.get_val(key)
            if key in ['Pop. Proportion', 'BPI Score', 'Normalized BPI Score']:
                val = format_percentage(val)
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

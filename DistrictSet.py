from copy import deepcopy

from helper import generate_bpi_data, generate_data


class DistrictSet:
    def __init__(self, districts, votes):
        self.districts = deepcopy(districts)
        self.votes = votes
        self.min_deviation = 999999
        self.max_deviation = 0
        self.franklin = 0
        self.norm_sum = 0
        self.update_districts(self.districts)

    def update_districts(self, districts):
        self.districts = deepcopy(districts)
        self.min_deviation = 999999
        self.max_deviation = 0
        self.franklin = 0
        self.norm_sum = 0
        self.generate_data()
        self.set_min_max()
        self.franklin_score()
        self.norm_sum_score()

    def set_min_max(self):
        for district in self.districts:
            self.min_deviation = min(self.min_deviation, district.norm_bpi)
            self.max_deviation = max(self.max_deviation, district.norm_bpi)

    def franklin_score(self):
        self.franklin = self.max_deviation - self.min_deviation

    def norm_sum_score(self):
        for district in self.districts:
            self.norm_sum += abs(district.norm_bpi)

    def clone(self):
        new_districts = []
        for district in self.districts:
            new_districts.append(district.clone())
        return DistrictSet(new_districts, self.votes)

    def get_district_list(self):
        return self.districts

    def generate_data(self):
        total_population = 0
        for district in self.districts:
            total_population += district.population
        for district in self.districts:
            district.set_val('Pop. Proportion',
                             district.population/total_population)
            district.set_val(
                '# Votes / Member', district.population_proportion*self.votes)

        self.districts = generate_bpi_data(self.get_district_list())
        for district in self.districts:
            district.norm_bpi = district.bpi - district.population_proportion

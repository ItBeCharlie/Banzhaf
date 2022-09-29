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
        self.generate_data()
        self.update_districts(self.districts)

    def update_districts(self, districts):
        self.districts = deepcopy(districts)
        self.min_deviation = 999999
        self.max_deviation = 0
        self.franklin = 0
        self.norm_sum = 0
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

    def override_votes(self, districts, vote_scale):
        for index, district in enumerate(self.districts):
            district.votes_per_member = int(
                districts[index].votes_per_member * vote_scale)
        print(self.sum_of_votes())
        self.fix_votes()
        print(self.sum_of_votes())

    def sum_of_votes(self):
        count = 0
        for district in self.districts:
            count += district.votes_per_member
        return count

    def min_votes_district(self):
        min_district = self.districts[0]
        for district in self.districts:
            if district.norm_bpi < min_district.norm_bpi:
                min_district = district
        return min_district

    def max_votes_district(self):
        max_district = self.districts[0]
        for district in self.districts:
            if district.norm_bpi > max_district.norm_bpi:
                max_district = district
        return max_district

    def fix_votes(self):
        count = self.sum_of_votes()
        while count < self.votes:
            self.min_votes_district().votes_per_member += 1
            count += 1
            self.districts = generate_bpi_data(self.get_district_list())
            for district in self.districts:
                district.norm_bpi = district.bpi - district.population_proportion
        while count > self.votes:
            self.max_votes_district().votes_per_member -= 1
            count -= 1
            self.districts = generate_bpi_data(self.get_district_list())
            for district in self.districts:
                district.norm_bpi = district.bpi - district.population_proportion

    def display_table(self, keys):
        # table_data = generate_table_data(districts, votes, len(key), bpi)
        table_data = []
        print_data = []
        max_lengths = dict.fromkeys(keys)

        for key in keys:
            max_lengths[key] = len(key)

        for district in self.districts:
            cur_data = district.print_data(keys)
            print_data.append(cur_data)
            for key in keys:
                max_lengths[key] = max(max_lengths[key], len(cur_data[key]))

        # print(max_lengths)

        separator_string = ''

        for key in max_lengths:
            separator_string += f'+-{"":-<{max_lengths[key]}}-'
        separator_string += '+'
        print(separator_string)

        for key in keys:
            print(f'| {key:<{max_lengths[key]}} ', end='')
        print('|')

        print(separator_string)

        for row, data in enumerate(print_data, start=1):
            for key in keys:
                print(f'| {data[key]:<{max_lengths[key]}} ', end='')
            print('|')
            if row % 5 == 0 and row < len(print_data):
                print(separator_string)

        print(separator_string, end='\n\n')

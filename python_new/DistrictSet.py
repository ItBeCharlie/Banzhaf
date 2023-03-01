from copy import deepcopy

from helper import generate_bpi_data, generate_data


class DistrictSet:
    def __init__(self, districts, votes, initial=False):
        """
        _districts: List of District Objects

        _votes: Number of votes in this system
        """
        self._districts = self.update_districts(districts)
        self._votes = votes
        self.generate_data(update_votes=initial, update_pop_prop=initial)

    @property
    def districts(self):
        return self._districts

    @districts.setter
    def districts(self, value):
        self._districts = value

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, value):
        self._votes = value

    def update_districts(self, districts):
        """
        Sets self._districts to a pointer clean copy of the districts in districts and updates the calculated data
        """
        self._districts = []
        for district in districts:
            self._districts.append(district.clone())
    #     self.update_data()

    # def update_data(self):
    #     self.franklin_score()
    #     self.norm_sum_score()

    # def get_val(self, key='Normalized BPI Score'):
    #     if key == 'Votes':
    #         return self.votes
    #     elif key == 'Min Deviation':
    #         return self.min_deviation
    #     elif key == 'Max Deviation':
    #         return self.max_deviation
    #     elif key == 'Franklin':
    #         return self.franklin
    #     elif key == 'Normalized BPI Score':
    #         return self.norm_sum

    def franklin_score(self):
        """
        Returns the franklin score, which is calculated by adding the absolute value of the two largest outliers from a districts bpi_diff
        """
        top = [0, 0]
        for district in self._districts:
            diff = abs(district.bpi_diff())
            if diff > top[1]:
                top[1] = diff
            elif diff > top[0]:
                top[0], top[1] = top[1], diff

        self.franklin = top[1] + top[0]

    def bpi_diff_score(self):
        """
        Returns the sum of all district bpi_diffs 
        """
        sum = 0
        for district in self._districts:
            sum += abs(district.bpi_diff())
        return sum

    def clone(self):
        """
        Returns a pointer safe clone of the DistrictSet
        """
        new_districts = []
        for district in self._districts:
            new_districts.append(district.clone())
        new_set = DistrictSet(new_districts, self._votes)
        # new_set.override_votes(new_districts)
        return new_set

    def generate_data(self, update_votes=False, update_pop_prop=False, quota=None):
        if quota == None:
            quota = self.votes//2+1
        if update_pop_prop:
            total_population = 0
            for district in self.districts:
                total_population += district.population
            for district in self.districts:
                district.set_val('Pop. Proportion',
                                 district.population/total_population)
        if update_votes:
            for district in self.districts:
                district.set_val(
                    '# Votes / Member', district.population_proportion*self.votes)

        generate_bpi_data(self, quota)
        for district in self.districts:
            district.norm_bpi = district.bpi - district.population_proportion

        self.update_data()

    def override_votes(self, district_set):
        """
        Adjusts the current votes to the votes of the district_set that is passed

        Then by comparing the votes between the two sets, it will adjust the _votes_per_member of the districts in the current district_set

        After the adjustment, self.fix_votes() is called to bring the number of votes back to the correct value
        """
        print(self.votes(), district_set.votes())
        vote_scale = self.votes() / district_set.votes()
        print(vote_scale)

        # TODO: THIS WILL NEED TO BE CHANGED
        self.sort_districts('District')
        district_set.sort_districts('District')

        for index, district in enumerate(self.districts()):
            district.votes_per_member(
                district_set.districts()[index].votes_per_member() * vote_scale)
        self.fix_votes()
        self.generate_data()

    def sum_of_votes(self):
        """
        Returns the sum of all the _votes_per_member for each district in self._districts
        """
        count = 0
        for district in self._districts:
            count += district.votes_per_member()
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
        # print("votes", count)
        for district in self.districts:
            if district.votes_per_member == 0:
                district.votes_per_member = 1

        while count < self.votes:
            self.min_votes_district().votes_per_member += 1
            count += 1
            generate_bpi_data(self, self.votes//2+1)
            for district in self.districts:
                district.norm_bpi = district.bpi - district.population_proportion
        while count > self.votes:
            self.max_votes_district().votes_per_member -= 1
            count -= 1
            generate_bpi_data(self, self.votes//2+1)
            for district in self.districts:
                district.norm_bpi = district.bpi - district.population_proportion
        # print("votes done", count)

    def display_table(self, keys):
        print_data = []
        max_lengths = dict.fromkeys(keys)

        for key in keys:
            if key == 'BPI Score':
                max_lengths[key] = len('Normalized BPI')
            elif key == 'Normalized BPI Score':
                max_lengths[key] = len('BPI Diff')
            else:
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
            if key == 'BPI Score':
                print(f'| {"Normalized BPI":<{max_lengths[key]}} ', end='')
            elif key == 'Normalized BPI Score':
                print(f'| {"BPI Diff":<{max_lengths[key]}} ', end='')
            else:
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

    def sort_districts(self, key='District', reverse=False):
        """
        ## Valid Keys:
        District | 
        Population | 
        Pop. Proportion | 
        '# Votes / Member' | 
        Normalized BPI Score | 
        BPI Score | 
        """
        self.districts.sort(key=lambda x: x.get_val(key), reverse=reverse)

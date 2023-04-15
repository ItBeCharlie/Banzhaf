from copy import deepcopy
from bpi import calc_bpi
import datetime


class DistrictSet:
    def __init__(self, districts, votes, date, initial=False, clone=False):
        """
        _districts: List of District Objects

        _votes: Number of votes in this system
        """
        self._districts = self.update_districts(districts)
        self._votes = votes
        self._date = date
        if not clone:
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
        new_set = DistrictSet(new_districts, self.votes(),
                              self.date(), clone=True)
        # new_set.override_votes(new_districts)
        return new_set

    def generate_data(self, update_votes=False, update_pop_prop=False, quota=None):
        # If no quota, set to 50%+1
        if quota == None:
            quota = self.votes()//2+1

        if update_pop_prop:
            total_population = 0
            for district in self.districts():
                total_population += district.population()
            for district in self.districts():
                district.population_proportion(
                    district.population()/total_population)
        if update_votes:
            for district in self.districts:
                district.votes_per_member(
                    district.population_proportion()*self.votes())

        self.calculate_bpi_data(quota)

    def calculate_bpi_data(self, quota):
        """
        Call the BPI algorithm, recompute the indexes for each district, and update the new bpi diffs
        """
        # Formating the data for the BPI calculator
        # Extract the votes from each district into a seperate list
        district_votes = []
        for district in self.districts():
            district_votes.append(district.votes_per_member())

        # Calculate the normalized bpis
        new_bpis = calc_bpi(quota, district_votes)

        # Set the BPIs and calculate the diffs
        for index, district in enumerate(self.districts):
            district.norm_bpi(new_bpis[index])
            district.bpi_diff(district.norm_bpi() -
                              district.population_proportion())

    def override_votes(self, new_votes):
        """
        Adjusts the current votes to the desired number of votes new_votes

        Adjusts the _votes_per_member of the districts in the current district_set by the ratio between new_votes and the current votes

        After the adjustment, self.fix_votes() is called to bring the number of votes back to the correct value
        """
        print(new_votes, self.votes())

        # Get the ratio between new and current votes
        vote_scale = new_votes / self.votes()
        print(vote_scale)

        # Set the votes to be the new_votes
        self.votes(new_votes)

        # Scale the votes for each district by this ratio as a first approximation
        for district in self.districts():
            district.votes_per_member(district.votes_per_member() * vote_scale)

        # Fix the votes to be the exact value of new votes
        self.fix_votes()
        self.generate_data()

    def sum_of_votes(self):
        """
        Returns the sum of all the _votes_per_member for each district in self._districts
        """
        count = 0
        for district in self.districts():
            count += district.votes_per_member()
        return count

    def min_norm_bpi_district(self):
        """
        Returns the district with the lowest norm_bpi
        """
        min_district = self.districts()[0]
        for district in self.districts():
            if district.norm_bpi() < min_district.norm_bpi():
                min_district = district
        return min_district

    def max_norm_bpi_district(self):
        """
        Returns the district with the highest norm_bpi
        """
        max_district = self.districts()[0]
        for district in self.districts():
            if district.norm_bpi() > max_district.norm_bpi():
                max_district = district
        return max_district

    def fix_votes(self):
        """
        After adjusting votes to new scale, balances votes to make sure it is equal to total number of votes for the current iteration
        """
        count = self.sum_of_votes()
        # print("votes", count)

        # Make sure there are no districts with 0 votes
        for district in self.districts():
            if district.votes_per_member() == 0:
                district.votes_per_member(1)
                count += 1

        # If the count is less than the votes required, add votes to the lowest district
        while count < self.votes():
            # Find district with lowest norm_bpi
            min_district = self.min_norm_bpi_district()
            # Add vote to that district
            min_district.votes_per_member(min_district.votes_per_member()+1)
            # Update current total of votes
            count += 1
            # Calculate bpi based on current number of votes as quota parameter (changed from total votes previously)
            self.calculate_bpi_data(count//2+1)

        # If the count is less than the votes required, add votes to the highest district
        while count > self.votes():
            # Find district with highest norm_bpi
            max_district = self.max_norm_bpi_district()
            # Subtract vote from that district
            max_district.votes_per_member(max_district.votes_per_member()-1)
            # Update current total of votes
            count -= 1
            # Calculate bpi based on current number of votes as quota parameter (changed from total votes previously)
            self.calculate_bpi_data(count//2+1)
        # print("votes done", count)

    def create_csv(self, outfile=None):
        """
        Creates a timestamped CSV containing the data of this DistrictSet
        """
        if outfile == None:
            outfile = f'{self.date()}-{self.votes()}'
        headers = ['District Name', 'Population', 'Population Proportion',
                   'Votes Per Member', 'Normalized BPI', 'BPI Diff']

        open(outfile, 'w').close()
        with open(outfile, 'w') as f:
            f.write(f'50% BPI Sum,{self.norm_sum():0.7%}\n')
            f.write(f'50% Franklin,{self.franklin():0.7%}\n')
            # f.write(f'2/3 BPI Sum,{two_thirds_district_set.norm_sum:0.7%}\n')
            # f.write(f'2/3 Franklin,{two_thirds_district_set.franklin:0.7%}\n')
            f.write(f'Total Votes,{self.votes()}\n')
            f.write(
                'District Name,Population,Population Proportion,Votes Per Member,Normalized BPI,BPI Diff\n')
            for district in self.districts():
                data = district.print_data()
                out_str = ''
                for item in data:
                    out_str += f'{data[item]},'
                f.write(f'{out_str[:-1]}\n')
            f.close()

    def display_csv(self, infile):
        with open(infile) as f:
            lines = f.readlines()

        # Comma Seperated List extracted from CSV
        cs_list = []
        for line in lines:
            cs_list.append(line.removesuffix('\n').split(','))

        # Table skips the header information
        table = cs_list[3:]
        print(f'Total Votes: {cs_list[2][1]}')

        # Figure out the max width of each column
        max_widths = [0]*len(table[0])
        for col in len(table):
            max_widths[col] = max(list(map(lambda row: len(row[col]), table)))

        # Build the seperator string
        for index in max_widths:
            separator_string += f'+-{"":-<{max_widths[index]}}-'
        separator_string += '+'

        # Print the table
        for row in table:
            for index, col in enumerate(row):
                print(f'| {col:<{max_widths[index]}} ', end='')
            print('|')
            if row % 5 == 0 and row < len(table):
                print(separator_string)
        print(separator_string)

        # Print other information
        for index in range(2):
            print(f'{cs_list[index][0]}: {cs_list[index][1]}')
        print()

    def sort_districts(self, key='id', reverse=False):
        """
        Reorders the districts list based on the specified key

        ## Valid Keys:
        id (default)
        bpi_diff
        """
        if key == 'id':
            self.districts.sort(key=lambda x: x.id(), reverse=reverse)
        elif key == 'bpi_diff':
            self.districts.sort(key=lambda x: x.bpi_diff(), reverse=reverse)

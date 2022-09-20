from District import District
from helper import generate_bpi_data
from helper import display_table
from helper import generate_data
import copy


class IterDistrict:
    def __init__(self, district):
        self.district = district

    def compare_to(self, other_district, key='norm_bpi'):
        match key:
            case 'norm_bpi':
                if self.get_norm() < other_district.get_norm():
                    return -1
                elif self.get_norm() > other_district.get_norm():
                    return 1
                return 0
            case 'number':
                return self.district.number - other_district.district.number

    def get_norm(self):
        return self.district.norm_bpi


def iterate(districts):
    clean_districts = copy.deepcopy(districts)
    iter_districts = []
    for district in clean_districts:
        iter_districts.append(IterDistrict(district))

    # iter_districts_sorted = sort_iter_districts(iter_districts)

    max_iterations = 10000
    cur_iteration = 0
    while cur_iteration < max_iterations:
        sort_iter_districts(iter_districts)

        # for d in iter_districts:
        #     print(round(d.district.norm_bpi, 5), end=' ')
        # print()
        old_sum = sum_norm_bpi(iter_districts)
        min_index = 0
        max_index = len(iter_districts)-1

        cur_sums = {}

        advance = False
        while not advance:
            new_iter_districts = step(
                iter_districts, min_index, max_index, trace=False)

            new_sum = sum_norm_bpi(new_iter_districts)

            cur_sums[new_sum] = copy.deepcopy(new_iter_districts)

            if new_sum > old_sum:
                # Go to next min/max index, whichever is a higher score
                iter_districts[min_index].district.votes_per_member -= 1
                iter_districts[max_index].district.votes_per_member += 1
                if abs(iter_districts[min_index+1].get_norm()) > abs(iter_districts[max_index-1].get_norm()):
                    min_index += 1
                else:
                    max_index -= 1
                print(min_index, max_index)
                if min_index >= max_index:
                    # Go with the best sum this step iteration
                    max_sum = 0
                    for key in cur_sums:
                        max_sum = max(max_sum, key)
                    new_iter_districts = cur_sums[max_sum]
                    advance = True

            sort_iter_districts(iter_districts)

        iter_districts = new_iter_districts

        cur_iteration += 1
        reorder_iter_district_list(iter_districts)
        display_table(iter_to_normal_districts(iter_districts), ['District', 'Population', 'Pop. Proportion',
                                                                 '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    return iter_to_normal_districts(iter_districts)


def step(iter_districts, min_index, max_index, trace=False):
    if trace:
        print(
            f'Min: {str(iter_districts[min_index].district.number)} | {str(iter_districts[min_index].district.norm_bpi*100)}')
        print(
            f'Max: {str(iter_districts[max_index].district.number)} | {str(iter_districts[max_index].district.norm_bpi*100)}', end='\n\n')
    iter_districts[min_index].district.votes_per_member += 1
    iter_districts[max_index].district.votes_per_member -= 1

    reorder_iter_district_list(iter_districts)

    normal_districts = iter_to_normal_districts(iter_districts)

    new_districts = generate_bpi_data(normal_districts)
    new_districts = generate_data(
        new_districts, keys=['Normalized BPI Score'])

    iter_districts = []
    for district in new_districts:
        iter_districts.append(IterDistrict(district))

    return iter_districts


def sort_iter_districts(districts):
    districts.sort(key=lambda x: x.district.norm_bpi, reverse=False)


# def sort_iter_districts_old(districts):
#     for i in range(len(districts)):
#         for j in range(len(districts)-i-1):
#             if districts[j].compare_to(districts[j+1]) < 0:
#                 districts[j], districts[j+1] = districts[j+1], districts[j]


def reorder_iter_district_list(districts):
    districts.sort(key=lambda x: x.district.number, reverse=False)


# def reorder_iter_district_list_old(districts):
#     for i in range(len(districts)):
#         for j in range(len(districts)-i-1):
#             if districts[j].compare_to(districts[j+1], key='number') > 0:
#                 districts[j], districts[j+1] = districts[j+1], districts[j]


def iter_to_normal_districts(iter_districts):
    districts = []
    for district in iter_districts:
        districts.append(district.district)
    return districts


def sum_norm_bpi(iter_districts):
    sum = 0
    for district in iter_districts:
        sum += abs(district.district.norm_bpi)
    return sum

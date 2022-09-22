from District import District
from helper import generate_bpi_data
from helper import display_table
from helper import generate_data
from helper import franklin_deviation
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

    def copy_self(self):
        return IterDistrict(self.district.copy_self())


def iterate(districts, trace=False):
    # clean_districts = copy_districts(districts)
    iter_districts = []
    for district in districts:
        iter_districts.append(IterDistrict(district.copy_self()))

    # iter_districts_sorted = sort_iter_districts(iter_districts)

    best_sum = sum_norm_bpi(iter_districts)
    original_sum = best_sum
    best_config = copy_iter_districts(iter_districts)

    max_iterations = 1000
    cur_iteration = 0
    while cur_iteration < max_iterations:
        if cur_iteration % 100 == 0:
            print(cur_iteration)
        sort_iter_districts(iter_districts)

        # for d in iter_districts:
        #     print(round(d.district.norm_bpi, 5), end=' ')
        # print()
        old_sum = sum_norm_bpi(iter_districts)
        min_index = 0
        max_index = len(iter_districts)-1

        cur_sums = {}

        advance = False
        count = 0
        while not advance:
            count += 1
            # print(count)

            new_iter_districts, valid_iter_district = step(
                copy_iter_districts(iter_districts), min_index, max_index, trace=trace)

            if valid_iter_district:
                new_sum = sum_norm_bpi(new_iter_districts)
                cur_sums[new_sum] = copy_iter_districts(new_iter_districts)
            if trace:
                display_copy = copy_iter_districts(new_iter_districts)

                sort_iter_districts(display_copy)
                print(
                    f'Min Index: {display_copy[min_index].district.number}\nMax Index: {display_copy[max_index].district.number}')
                if valid_iter_district:
                    print(f'Sum: {new_sum*100}\n')
                else:
                    print()

            if trace:
                display_table(iter_to_normal_districts(display_copy), [
                    'District', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

            # reorder_iter_district_list(new_iter_districts)

            # if new_sum > old_sum:

            # Go to next min/max index, whichever is a higher score

            # Step approach
            if abs(iter_districts[min_index+1].get_norm()) > abs(iter_districts[max_index-1].get_norm()):
                min_index += 1
            else:
                max_index -= 1

            if min_index >= max_index:
                # Go with the best sum this step iteration
                min_sum = 999999999999999999
                for key in cur_sums:
                    min_sum = min(min_sum, key)
                if trace:
                    print(f'Keys: {cur_sums.keys()}\nMin Sum: {min_sum}\n')
                new_iter_districts = copy_iter_districts(cur_sums[min_sum])
                advance = True

        iter_districts = new_iter_districts

        sort_iter_districts(iter_districts)

        if trace:
            print(f'Old Sum: {old_sum}\nNew Sum: {min_sum}\n')

        reorder_iter_district_list(iter_districts)

        if min_sum <= best_sum:
            best_config = copy_iter_districts(iter_districts)

        cur_iteration += 1

        if trace:
            display_table(iter_to_normal_districts(iter_districts), ['District', 'Population', 'Pop. Proportion',
                                                                     '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    print(f'Original Sum: {original_sum}\nBest Sum:     {best_sum}\n\nOriginal Frankin: {franklin_deviation(districts)}\nNew Franklin:     {franklin_deviation(iter_to_normal_districts(best_config))}\n')

    display_table(districts, ['District', 'Population', 'Pop. Proportion',
                                                        '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    return iter_to_normal_districts(best_config)


def step(iter_districts, min_index, max_index, trace=False):
    if trace:
        print(
            f'Min: {str(iter_districts[min_index].district.number)} | {str(iter_districts[min_index].district.norm_bpi*100)}')
        print(
            f'Max: {str(iter_districts[max_index].district.number)} | {str(iter_districts[max_index].district.norm_bpi*100)}', end='\n\n')

    iter_districts[min_index].district.votes_per_member += 1
    iter_districts[max_index].district.votes_per_member -= 1
    if iter_districts[max_index].district.votes_per_member < 2:
        return iter_districts, False
    reorder_iter_district_list(iter_districts)

    normal_districts = iter_to_normal_districts(iter_districts)

    new_districts = generate_bpi_data(normal_districts)
    new_districts = generate_data(
        new_districts, keys=['Normalized BPI Score'])

    iter_districts = []
    for district in new_districts:
        iter_districts.append(IterDistrict(district))

    return iter_districts, True


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


def copy_districts(districts):
    new_districts = []
    for district in districts:
        new_districts.append(district.copy_self())
    return new_districts


def copy_iter_districts(iter_districts):
    new_iter_districts = []
    for district in iter_districts:
        new_iter_districts.append(district.copy_self())
    return new_iter_districts

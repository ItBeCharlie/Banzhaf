from helper import *
import time


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

    def clone(self):
        return IterDistrict(self.district.clone())


def iterate(districts, trace=False, iterations=200):
    # clean_districts = copy_districts(districts)
    iter_districts = []
    for district in districts:
        iter_districts.append(IterDistrict(district.clone()))

    # iter_districts_sorted = sort_iter_districts(iter_districts)

    best_sum = sum_norm_bpi(iter_districts)
    original_sum = best_sum
    best_config = copy_iter_districts(iter_districts)

    max_iterations = iterations
    time_steps = 20
    cur_iteration = 0
    display_step = max_iterations // time_steps
    print()
    start_time = time.perf_counter()
    while cur_iteration < max_iterations:
        if (cur_iteration) % display_step == 0:
            print(
                f'\r[{"@"*(cur_iteration//display_step)}{"-"*((max_iterations//display_step)-(cur_iteration//display_step))}]', end='')
        sort_iter_districts(iter_districts)

        # for d in iter_districts:
        #     print(round(d.district.norm_bpi, 5), end=' ')
        # print()
        old_sum = sum_norm_bpi(iter_districts)
        min_index = -1
        max_index = -1

        cur_sums = {}

        advance = False
        # count = 0
        while not advance:
            # if cur_iteration > max_iterations * 1.1:
            #     min_index, max_index = walk_down_approach(
            #         iter_districts, min_index, max_index)
            # else:
            min_index, max_index = brute_force_approach(
                iter_districts, min_index, max_index)

            if min_index >= max_index:
                # Go with the best sum this step iteration
                min_sum = 999999999999999999
                # if len(cur_sums) == 0:
                #     new_iter_districts = iter_districts
                #     cur_iteration = max_iterations
                #     advance = True
                #     continue
                for key in cur_sums:
                    min_sum = min(min_sum, key)
                if trace:
                    print(f'Keys: {cur_sums.keys()}\nMin Sum: {min_sum}\n')
                new_iter_districts = copy_iter_districts(cur_sums[min_sum])
                advance = True
                continue

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

        iter_districts = new_iter_districts

        sort_iter_districts(iter_districts)

        if trace:
            print(f'Old Sum: {old_sum}\nNew Sum: {min_sum}\n')

        reorder_iter_district_list(iter_districts)

        if min_sum < best_sum:
            best_config = copy_iter_districts(iter_districts)
            best_sum = min_sum

        cur_iteration += 1

        if trace:
            display_table(iter_to_normal_districts(iter_districts), ['District', 'Population', 'Pop. Proportion',
                                                                     '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
    end_time = time.perf_counter()

    print(f'\r[{"@"*(max_iterations//display_step)}]')
    print(f'Total time: {end_time-start_time}s')

    print(f'Original Sum: {format_percentage(original_sum, 10)}\nBest Sum:     {format_percentage(best_sum, 10)}\n\nOriginal Frankin: {format_percentage(franklin_deviation(districts), 10)}\nNew Franklin:     {format_percentage(franklin_deviation(iter_to_normal_districts(best_config)), 10)}\n')

    # display_table(districts, ['District', 'Population', 'Pop. Proportion',
    # '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    display_table(iter_to_normal_districts(best_config), ['District', 'Population', 'Pop. Proportion',
                                                          '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    return iter_to_normal_districts(best_config)


def walk_down_approach(iter_districts, min_index, max_index):
    # Walk down approach
    if min_index == -1 and max_index == -1:
        return 0, len(iter_districts)-1
    if abs(iter_districts[min_index+1].get_norm()) > abs(iter_districts[max_index-1].get_norm()):
        min_index += 1
    else:
        max_index -= 1

    return min_index, max_index


def brute_force_approach(iter_districts, min_index, max_index):
    if min_index == -1 and max_index == -1:
        return 0, len(iter_districts)-1
    if min_index < max_index-1:
        min_index += 1
    else:
        min_index = 0
        max_index -= 1

    return min_index, max_index


def step(iter_districts, min_index, max_index, trace=False):
    if trace:
        print(
            f'Min: {str(iter_districts[min_index].district.number)} | {str(iter_districts[min_index].district.norm_bpi*100)} | {min_index}')
        print(
            f'Max: {str(iter_districts[max_index].district.number)} | {str(iter_districts[max_index].district.norm_bpi*100)} | {max_index}', end='\n\n')

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

from xmlrpc.client import Boolean
from helper import *
from DistrictSet import DistrictSet
import time


def iterate(districts: DistrictSet, trace=False, iterations=200, score_metric='Normalized BPI Score'):
    # clean_districts = copy_districts(districts)
    iter_districts = districts.clone()

    iter_districts.display_table(['District', 'Population', 'Pop. Proportion',
                                  '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    # iter_districts = []
    # for district in districts:
    #     iter_districts.append(IterDistrict(district.clone()))

    # iter_districts_sorted = sort_iter_districts(iter_districts)

    best_score = iter_districts.get_val(key=score_metric)
    original_score = best_score
    best_config = iter_districts.clone()

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

        iter_districts.sort_districts(key='Normalized BPI Score')

        # for d in iter_districts:
        #     print(round(d.district.norm_bpi, 5), end=' ')
        # print()
        old_score = iter_districts.get_val(key=score_metric)
        min_index = -1
        max_index = -1

        cur_scores = {}

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
                min_score = 999999999999999999
                # if len(cur_sums) == 0:
                #     new_iter_districts = iter_districts
                #     cur_iteration = max_iterations
                #     advance = True
                #     continue
                for key in cur_scores:
                    min_score = min(min_score, key)
                if trace:
                    print(f'Keys: {cur_scores.keys()}\nMin Sum: {min_score}\n')
                new_iter_districts = cur_scores[min_score].clone()
                advance = True
                continue

            new_iter_districts, valid_iter_district = step(
                iter_districts.clone(), min_index, max_index, trace=trace)

            if valid_iter_district:
                new_score = new_iter_districts.get_val(key=score_metric)
                cur_scores[new_score] = new_iter_districts.clone()
            if trace:
                display_copy = new_iter_districts.clone()

                display_copy.sort_districts('District')
                print(
                    f'Min Index: {display_copy.districts[min_index].number}\nMax Index: {display_copy.districts[max_index].number}')
                if valid_iter_district:
                    print(f'Sum: {new_score*100}\n')
                else:
                    print()

            if trace:
                display_copy.display_table([
                    'District', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

            # reorder_iter_district_list(new_iter_districts)

            # if new_sum > old_sum:

        iter_districts = new_iter_districts

        iter_districts.update_data()

        # iter_districts.sort_districts(key='Normalized BPI Score')

        if trace:
            print(f'Old Sum: {old_score}\nNew Sum: {min_score}\n')

        iter_districts.sort_districts(key='District')

        if min_score < best_score:
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            iter_districts.display_table(['District', 'Population', 'Pop. Proportion',
                                          '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
            best_config = iter_districts.clone()
            # best_config.display_table([
            # 'District', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
            best_score = min_score

        cur_iteration += 1

        if trace:
            iter_districts.display_table(['District', 'Population', 'Pop. Proportion',
                                          '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
    end_time = time.perf_counter()

    print(f'\r[{"@"*(max_iterations//display_step)}]')
    print(f'Total time: {end_time-start_time}s')

    print(f'Original Score: {format_percentage(original_score, 10)}\nBest Score:     {format_percentage(best_score, 10)}\n\nOriginal Frankin: {format_percentage((districts.franklin), 10)}\nNew Franklin:     {format_percentage((best_config.franklin), 10)}\n')

    # display_table(districts, ['District', 'Population', 'Pop. Proportion',
    # '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    best_config.display_table(['District', 'Population', 'Pop. Proportion',
                               '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    return best_config


def walk_down_approach(iter_districts, min_index, max_index, score_metric):
    # Walk down approach
    if min_index == -1 and max_index == -1:
        return 0, len(iter_districts.districts)-1
    if score_metric == 'Normalized BPI Score':
        if abs(iter_districts.districts[min_index+1].get_norm()) > abs(iter_districts.districts[max_index-1].get_norm()):
            min_index += 1
        else:
            max_index -= 1

    return min_index, max_index


def brute_force_approach(iter_districts, min_index, max_index):
    if min_index == -1 and max_index == -1:
        return 0, len(iter_districts.districts)-1
    if min_index < max_index-1:
        min_index += 1
    else:
        min_index = 0
        max_index -= 1

    return min_index, max_index


def step(iter_districts: DistrictSet, min_index, max_index, trace=False):
    if trace:
        print(
            f'Min: {str(iter_districts.districts[min_index].number)} | {str(iter_districts.districts[min_index].norm_bpi*100)} | {min_index}')
        print(
            f'Max: {str(iter_districts.districts[max_index].number)} | {str(iter_districts.districts[max_index].norm_bpi*100)} | {max_index}', end='\n\n')

    iter_districts.districts[min_index].votes_per_member += 1
    iter_districts.districts[max_index].votes_per_member -= 1
    if iter_districts.districts[max_index].votes_per_member < 2:
        return iter_districts, False

    iter_districts.sort_districts('District')

    iter_districts.generate_data(update_votes=False)

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

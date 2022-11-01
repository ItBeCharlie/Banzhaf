from math import dist
from helper import *
from DistrictSet import DistrictSet
import time
import random


def iterate(district_set: DistrictSet, trace=False, iterations=50, score_metric='Normalized BPI Score'):

    return step1(district_set, trace=trace,
                 iterations=iterations, score_metric=score_metric)


# Find the local minimum
def step1(district_set: DistrictSet, trace=False, iterations=50, score_metric='Normalized BPI Score'):
    orig_district_set = district_set.clone()
    district_set = district_set.clone()

    print('\n\n\n\n')
    district_set.display_table(['District', 'Population', 'Pop. Proportion',
                                '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    best_score = district_set.get_val(key=score_metric)
    original_score = best_score
    original_franklin = orig_district_set.franklin
    best_config = district_set.clone()

    number_of_districts = len(district_set.districts)

    votes_list_cache = []
    votes_list_cache.append(extract_votes(district_set))

    print()
    loading_bar(0, iterations)
    start_time = time.perf_counter()
    iteration = 0
    while iteration < iterations:
        loading_bar(iteration, iterations)

        district_set.sort_districts(key='Normalized BPI Score')

        min_index = 0
        max_index = len(district_set.districts) - 1

        old_score = district_set.get_val(key=score_metric)
        cur_scores = {}

        while max_index > min_index:
            new_district_set, valid_district_set = step(
                district_set.clone(), min_index, max_index, trace=trace)

            if valid_district_set:
                new_score = new_district_set.get_val(key=score_metric)
                cur_scores[new_score] = new_district_set.clone()

            if trace:
                display_copy = new_district_set.clone()

                display_copy.sort_districts('District')
                print(
                    f'Min Index: {display_copy.districts[min_index].number}\nMax Index: {display_copy.districts[max_index].number}')
                if valid_district_set:
                    print(f'Score: {new_score*100}\n')
                else:
                    print()

                display_copy.display_table([
                    'District', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

            min_index, max_index = brute_force_approach(
                number_of_districts, min_index, max_index)

        min_score = 9999999
        cur_scores_keys = (list(cur_scores.keys()))
        cur_scores_keys.sort()
        # for key in cur_scores:
        #     min_score = min(min_score, key)
        #     if trace:
        #         print(f'Keys: {cur_scores.keys()}\nMin Sum: {min_score}\n')

        min_score = cur_scores_keys[0]
        if random.random() < 0.2:
            # print(list(cur_scores.keys()))
            min_score = cur_scores_keys[1]
            # print('RAND')

        district_set = cur_scores[min_score].clone()

        district_set.update_data()

        if trace:
            print(f'Old Score: {old_score}\nNew Score: {min_score}\n')

        district_set.sort_districts(key='District')
        if min_score < best_score:
            # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            # district_set.display_table(['District', 'Population', 'Pop. Proportion', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
            best_config = district_set.clone()
            # best_config.display_table([
            # 'District', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
            best_score = min_score

        extracted_votes = extract_votes(district_set)
        if extracted_votes in votes_list_cache:
            break
        else:
            votes_list_cache.append(extracted_votes)

        if trace:
            district_set.display_table(['District', 'Population', 'Pop. Proportion',
                                        '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

        iteration += 1

    end_time = time.perf_counter()

    loading_bar(iteration, iterations)
    print(f'\nTotal time: {end_time-start_time}s')

    print(f'Original Score: {format_percentage(original_score, 10)}\nBest Score:     {format_percentage(best_score, 10)}\n\nOriginal Frankin: {format_percentage((original_franklin), 10)}\nNew Franklin:     {format_percentage((best_config.franklin), 10)}\n')

    # display_table(districts, ['District', 'Population', 'Pop. Proportion',
    # '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    best_config.display_table(['District', 'Population', 'Pop. Proportion',
                               '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    update_log('iterations', iteration, 'add', 'int')
    update_log('time', end_time-start_time, 'add', 'float')

    return best_config


def extract_votes(district_set):
    district_set = district_set.clone()
    district_set.sort_districts(key='District')
    votes_list = []
    for district in district_set.districts:
        votes_list.append(district.votes_per_member)
    return votes_list


def step(district_set: DistrictSet, min_index, max_index, trace=False):
    if trace:
        print(
            f'Min: {str(district_set.districts[min_index].number)} | {str(district_set.districts[min_index].norm_bpi*100)} | {min_index}')
        print(
            f'Max: {str(district_set.districts[max_index].number)} | {str(district_set.districts[max_index].norm_bpi*100)} | {max_index}', end='\n\n')

    district_set.districts[min_index].votes_per_member += 1
    district_set.districts[max_index].votes_per_member -= 1
    if district_set.districts[max_index].votes_per_member < 2:
        return district_set, False

    district_set.sort_districts('District')

    district_set.generate_data(update_votes=False, update_pop_prop=False)

    return district_set, True


def brute_force_approach(number_of_districts, min_index, max_index):
    if min_index == -1 and max_index == -1:
        return 0, number_of_districts-1
    if min_index < max_index-1:
        min_index += 1
    else:
        min_index = 0
        max_index -= 1

    return min_index, max_index


def loading_bar(cur_iteration, max_iterations):
    print(f'\rIterations: {cur_iteration} / {max_iterations}', end='')

from DistrictSet import DistrictSet
import random


def optimize(district_set: DistrictSet, trace=False, iterations=50):
    orig_district_set = district_set.clone()
    district_set = district_set.clone()

    # district_set.display_table(['District', 'Population', 'Pop. Proportion',
    # '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    # Current best score achieved by the optimizer
    best_score = district_set.bpi_diff_score()
    original_score = best_score
    original_franklin = orig_district_set.franklin_score()
    best_config = district_set.clone()

    number_of_districts = len(district_set.districts)

    # Used to ensure each iteration has a unique set of votes
    votes_list_cache = []
    votes_list_cache.append(extract_votes(district_set))

    print()
    iteration = 0
    while iteration < iterations:

        district_set.sort_districts(key='bpi_diff')

        min_index = 0
        max_index = number_of_districts - 1

        old_score = district_set.bpi_diff_score()
        cur_scores = {}

        while max_index > min_index:
            new_district_set, valid_district_set = step(
                district_set.clone(), min_index, max_index, trace=trace)

            if valid_district_set:
                new_score = new_district_set.bpi_score_diff()
                cur_scores[new_score] = new_district_set.clone()

            if trace:
                display_copy = new_district_set.clone()

                display_copy.sort_districts(key='id')
                print(
                    f'Min Index: {display_copy.districts()[min_index].id()}\nMax Index: {display_copy.districts()[max_index].id()}')
                if valid_district_set:
                    print(f'Score: {new_score*100}\n')
                else:
                    print()

                # display_copy.display_table([
                #     'District', '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

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

        if trace:
            print(f'Old Score: {old_score}\nNew Score: {min_score}\n')

        district_set.sort_districts(key='id')
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

    # print(f'Original Score: {format_percentage(original_score, 10)}\nBest Score:     {format_percentage(best_score, 10)}\n\nOriginal Frankin: {format_percentage((original_franklin), 10)}\nNew Franklin:     {format_percentage((best_config.franklin), 10)}\n')

    # display_table(districts, ['District', 'Population', 'Pop. Proportion',
    # '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    if best_config.franklin() > original_franklin:
        return orig_district_set
    return best_config


def extract_votes(input_district_set):
    district_set = input_district_set.clone()
    district_set.sort_districts(key='id')
    votes_list = []
    for district in district_set.districts():
        votes_list.append(district.votes_per_member())
    return votes_list


def step(district_set: DistrictSet, min_index, max_index, trace=False):
    if trace:
        print(
            f'Min: {str(district_set.districts()[min_index].id())} | {str(district_set.districts()[min_index].norm_bpi()*100)} | {min_index}')
        print(
            f'Max: {str(district_set.districts()[max_index].id())} | {str(district_set.districts()[max_index].norm_bpi()*100)} | {max_index}', end='\n\n')

    # Add a vote to the min_index district
    district_set.districts()[min_index].votes_per_member(
        district_set.districts()[min_index].votes_per_member()+1)
    # Subtract a vote to the max_index district
    district_set.districts()[max_index].votes_per_member(
        district_set.districts()[max_index].votes_per_member()-1)
    if district_set.districts()[max_index].votes_per_member() < 2:
        return district_set, False

    district_set.sort_districts(key='id')

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

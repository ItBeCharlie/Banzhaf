from bpi_old import calc_bpi_single
from helper import *
from District import District
from stepper import iterate
from testing_init import init
from DistrictSet import DistrictSet
import copy


def main():
    initialize_log_file()
    # districts = input_data()
    # votes = get_total_number_of_votes()
    districts, votes = init(4)
    districts = DistrictSet(districts, votes, initial=True)
    # districts = [10, 20, 30]
    # votes = 50                                                                             '# Votes / Member', 'Normalized BPI Score']))
    districts.display_table(['District', 'Population', 'Pop. Proportion',
                             '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    orig_districts = districts.clone()
    votes = 0

    prev_franklin = 99999
    threshold = 0.0001
    best_franklin = 99999
    best_set = districts.clone()

    print(
        f'Franklin: {districts.franklin:.10%}\nBPI Sum:  {districts.norm_sum:.10%}')

    district_sets = []
    two_thirds_district_sets = []
    print(f"\n{'='*97}\n\n")
    try:
        while votes < 500:

            votes += 100
            districts = DistrictSet(best_set.districts, votes, initial=True)

            districts.override_votes(best_set)

            districts = iterate(districts, iterations=50,
                                score_metric='Normalized BPI Score', trace=False)

            two_thirds_districts = districts.clone()
            two_thirds_districts.generate_data(
                quota=(two_thirds_districts.votes*2)//3)
            two_thirds_districts.franklin_score()

            print(
                f'2/3 Majority Franklin: {two_thirds_districts.franklin:.10%}')

            districts.display_table(['District', 'Population', 'Pop. Proportion',
                                     '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
            # two_thirds_districts.display_table(
            # ['District', 'BPI Score', 'Normalized BPI Score'])

            cur_franklin = districts.franklin
            if cur_franklin < best_franklin:
                best_franklin = cur_franklin
                best_set = districts.clone()
                best_two_thirds = copy.deepcopy(two_thirds_districts)
            print(f'Votes: {votes}')

            print(districts.franklin)
            print(two_thirds_districts.franklin)

            district_sets.append(districts.clone())
            two_thirds_district_sets.append(
                copy.deepcopy(two_thirds_districts))

            print(district_sets[-1].franklin)
            print(two_thirds_district_sets[-1].franklin)

            generate_csv(districts, two_thirds_districts, f'csvs/{votes}.csv')

            print(f"\n{'='*97}\n\n")
    except Exception as e:
        print(f'\n{e}')
        print('Error or run terminated')

    for index, district_set in enumerate(district_sets):
        print(
            f'BPI Sum:  {district_set.norm_sum:.10%}\nFranklin: {district_set.franklin:.10%}\n2/3 Majority Franklin: {two_thirds_district_sets[index].franklin:.10%}\nTotal Votes: {best_set.votes}')
        district_set.display_table(['District', 'Population', 'Pop. Proportion',
                                    '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])
        print(f"\n{'='*97}\n\n")

    print(
        f'BPI Sum: {best_set.norm_sum:.10%}\nFranklin: {best_set.franklin:.10%}\n2/3 Majority Franklin: {best_two_thirds.franklin:.10%}\nTotal Votes: {best_set.votes}')
    best_set.display_table(['District', 'Population', 'Pop. Proportion',
                            '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    generate_csv(best_set, best_two_thirds, 'csvs/best.csv')

    print(f'Total Calculation Time: {get_log("time")}s')
    print(f'Total Iterations: {get_log("iterations")}')


def generate_csv(district_set, two_thirds_district_set, outfile):
    keys = ['District',
            'Population',
            'Pop. Proportion',
            '# Votes / Member',
            'BPI Score',
            'Normalized BPI Score']
    open(outfile, 'w').close()
    with open(outfile, 'w') as f:
        f.write(f'50% BPI Sum,{district_set.norm_sum:0.7%}\n')
        f.write(f'50% Franklin,{district_set.franklin:0.7%}\n')
        f.write(f'2/3 BPI Sum,{two_thirds_district_set.norm_sum:0.7%}\n')
        f.write(f'2/3 Franklin,{two_thirds_district_set.franklin:0.7%}\n')
        f.write(f'Total Votes,{district_set.votes}\n')
        f.write(
            'District,Population,Pop. Proportion,# Votes / Member,50% Normalized BPI,50% BPI Diff, 2/3 Normalized BPI, 2/3 BPI Diff\n')
        for index, district in enumerate(district_set.districts):
            data = district.print_data(keys)
            # print(data)
            out_str = ''
            for item in data:
                out_str += f'{data[item]},'
            data = two_thirds_district_set.districts[index].print_data(['BPI Score',
                                                                        'Normalized BPI Score'])
            for item in data:
                out_str += f'{data[item]},'
            f.write(f'{out_str[:-1]}\n')
        f.close()


def input_data():
    districts = []
    is_number_good = False
    while not is_number_good:
        response = input('Enter number of districts: ')
        if is_int(response):
            if response == '0':
                print(
                    f'"{response}" is an invalid response. Please enter a positive whole number.')
            else:
                district_number = int(response)
                is_number_good = True

    for i in range(1, district_number+1):
        districts.append(District(i))

    current_district_index = 0
    while current_district_index < len(districts):
        current_district = districts[current_district_index]
        response = input(
            f'Enter population of District {current_district_index+1}: ')
        if current_district.change_population(response):
            current_district_index += 1

    is_data_good = False
    error = ''
    while not is_data_good:
        display_table(districts, ['District', 'Population'])
        if error != '':
            print(error)
            error = ''
        confirmation = input("Do you want to edit any district data? (Y/N): ")
        if confirmation == 'y':
            is_district_fixed = False
            while not is_district_fixed:
                response = input("Which district would you like to edit: ")
                if is_int(response):
                    district_index = int(response) - 1
                    if district_index >= len(districts) or district_index < 0:
                        print(
                            f'"{response}" is not a valid district. Please enter a positive whole number less than {str(len(districts) + 1)}')
                    else:
                        current_district = districts[district_index]
                        is_population_fixed = False
                        while not is_population_fixed:
                            new_population = input(
                                f'Please enter the new population for district {str(response)}: ')
                            if current_district.change_population(new_population):
                                is_population_fixed = True
                                is_district_fixed = True
                else:
                    print(
                        f'"{response}" is not a valid district. Please enter a positive whole number less than {str(len(districts) + 1)}')
        elif confirmation == 'n':
            is_data_good = True
        else:
            error = 'Invalid response, please enter "Y" or "N"'

    # display_table(['District', 'Population'])
    return districts


def get_total_number_of_votes():
    is_valid_votes = False
    while not is_valid_votes:
        votes = input("Please enter total number of votes: ")
        is_valid_votes = is_int(votes)
    return int(votes)


def initialize_log_file():
    open('log.csv', 'w').close()
    data = ['iterations', 'time']
    for d in data:
        update_log(d, 0)


main()

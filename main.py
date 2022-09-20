from bpi import calc_bpi_single
from helper import *
from District import District
from stepper import iterate
from testing_init import init


def main():
    # districts = input_data()
    # votes = get_total_number_of_votes()
    districts, votes = init(2)
    # districts = [10, 20, 30]
    # votes = 50
    districts = generate_data(districts, votes, ['District', 'Population',
                                                 'Pop. Proportion', '# Votes / Member'])

    display_table(districts, ['District', 'Population',
                  'Pop. Proportion', '# Votes / Member'])

    generate_bpi_data(districts)

    districts = generate_data(districts, votes, ['District', 'Population', 'Pop. Proportion',
                                                 '# Votes / Member', 'Normalized BPI Score'])

    display_table(districts, ['District', 'Population', 'Pop. Proportion',
                  '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    districts = iterate(districts)

    display_table(districts, ['District', 'Population', 'Pop. Proportion',
                  '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])


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


main()

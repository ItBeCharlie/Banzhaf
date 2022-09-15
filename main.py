from bpi import calc_bpi_single
from helper import *
from District import District

districts = []


def main():
    global districts
    input_data()
    votes = get_total_number_of_votes()
    # districts = [10, 20, 30]
    # votes = 50
    generate_data(votes, ['District', 'Population',
                  'Pop. Proportion', '# Votes / Member'])

    display_table(['District', 'Population',
                  'Pop. Proportion', '# Votes / Member'])

    generate_bpi_data()

    generate_data(votes, ['District', 'Population', 'Pop. Proportion',
                  '# Votes / Member', 'Normalized BPI Score'])

    display_table(['District', 'Population', 'Pop. Proportion',
                  '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])


def generate_bpi_data():
    global districts

    sum = 0
    bpi_data = []

    for district in districts:
        sum += district.votes_per_member
        bpi_data.append(district.votes_per_member)

    bpi_data.insert(0, sum//2)
    bpi = calc_bpi_single(bpi_data)
    for index, district in enumerate(districts):
        district.bpi = bpi[index]


def input_data():
    global districts
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
        display_table(['District', 'Population'])
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


def generate_data(votes, keys):
    global districts
    total_population = 0
    for district in districts:
        total_population += district.population
    for district in districts:
        for key in keys:
            match key:
                case 'Pop. Proportion':
                    district.set_val(key, district.population/total_population)
                case '# Votes / Member':
                    district.set_val(key, district.population_proportion*votes)
                case 'Normalized BPI Score':
                    district.set_val(key, district.bpi -
                                     district.population_proportion)


def get_total_number_of_votes():
    is_valid_votes = False
    while not is_valid_votes:
        votes = input("Please enter total number of votes: ")
        is_valid_votes = is_int(votes)
    return int(votes)


# def generate_table_data(districts, votes, key_len, bpi):
#     total_population = sum(districts)
#     table_data = []
#     for count, population in enumerate(districts, start=1):
#         if key_len > 3:
#             table_data.append([count, population, population/total_population])
#             table_data[count-1].append(int(table_data[count-1][2]*votes))
#         if key_len > 4:
#             table_data[count-1].append(bpi[count-1] - table_data[count-1][2])
#     return table_data


def display_table(keys):
    global districts
    # table_data = generate_table_data(districts, votes, len(key), bpi)
    table_data = []
    print_data = []
    max_lengths = dict.fromkeys(keys)

    for key in keys:
        max_lengths[key] = len(key)

    for district in districts:
        cur_data = district.print_data(keys)
        print_data.append(cur_data)
        for key in keys:
            max_lengths[key] = max(max_lengths[key], len(cur_data[key]))

    print(max_lengths)

    for key in max_lengths.keys():
        print(f'+-{"":-<{max_lengths[key]}}-', end='')
    print('+')

    for key in keys:
        print(f'| {key:<{max_lengths[key]}} ', end='')
    print('|')

    for key in max_lengths.keys():
        print(f'+-{"":-<{max_lengths[key]}}-', end='')
    print('+')

    for data in print_data:
        for key in keys:
            print(f'| {data[key]:<{max_lengths[key]}} ', end='')
        print('|')

    for key in max_lengths.keys():
        print(f'+-{"":-<{max_lengths[key]}}-', end='')
    print('+')

    return table_data


# def display_data():
#     global districts
#     # Counts the number of digits in the number of districts
#     # If there are 1000 districts: len("1000") = 4
#     district_total_digits = len(str(len(districts)))

#     # print(district_number)

#     print_str = 'District' + ' '*(district_total_digits+3) + '| Population'

#     print(print_str)
#     print('-' * (11 + district_total_digits) + '+' + '-' * 12)

#     # print("District".ljust(district_number + 3) + "Population")
#     for district in districts:
#         print("District " + str(district.number).rjust(district_total_digits) +
#               ": | " + str(district.population))


main()

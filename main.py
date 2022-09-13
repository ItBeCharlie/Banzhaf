from bpi import calc_bpi_single


def main():
    districts = input_data()
    votes = get_total_number_of_votes()
    # districts = [10, 20, 30]
    # votes = 50
    table_data = generate_table(districts, votes, [
                                'District', 'Population', 'Pop. Proportion', '# Votes / Member'], None)
    print(table_data)
    sum = 0
    bpi_data = []
    for data in table_data:
        sum += data[3]
        bpi_data.append(data[3])
    bpi_data.insert(0, sum//2)
    bpi = calc_bpi_single(bpi_data)
    table_data = generate_table(districts, votes, [
                                'District', 'Population', 'Pop. Proportion', '# Votes / Member', 'Normalized BPI Score'], bpi)


def input_data():
    districts = []
    is_number_good = False
    while not is_number_good:
        response = input('Enter number of districts: ')
        if response.isnumeric() and '.' not in response:
            district_number = int(response)
            districts = [0] * district_number
            is_number_good = True
        else:
            print('Please enter a positive whole number for number of districts "' + str(
                response) + '" is invalid.')
    current_district_index = 0
    current_district = current_district_index + 1

    while current_district_index < len(districts):
        response = input('Enter population of District ' +
                         str(current_district) + ": ")
        if response.isnumeric() and '.' not in response:
            population = int(response)
            districts[current_district_index] = population
            current_district_index += 1
            current_district = current_district_index + 1
        else:
            print('Please enter a positive whole number for population of district ' + str(current_district) + ', "' + str(
                response) + '" is invalid.')
    is_data_good = False
    error = ''
    while not is_data_good:
        display_data(districts)
        if error != '':
            print(error)
            error = ''
        confirmation = input("Do you want to edit any district data? (Y/N): ")
        if confirmation == 'y':
            is_district_fixed = False
            while not is_district_fixed:
                response = input("Which district would you like to edit: ")
                if response.isnumeric() and '.' not in response:
                    district_index = int(response) - 1
                    if district_index >= len(districts) or district_index < 0:
                        print(
                            '"' + response + '" is not a valid district. Please enter a positive whole number less than ' + str(len(districts) + 1))
                    else:
                        is_population_fixed = False
                        while not is_population_fixed:
                            new_population = input(
                                "Please enter the new population for district " + str(response) + ": ")
                            if new_population.isnumeric() and '.' not in new_population:
                                districts[district_index] = int(new_population)
                                is_population_fixed = True
                                is_district_fixed = True
                            else:
                                print('Please enter a positive whole number for population of district ' + str(response) + ', "' + str(
                                    new_population) + '" is invalid.')
                else:
                    print(
                        '"' + response + '" is not a valid district. Please enter a positive whole number less than ' + str(len(districts) + 1))
        elif confirmation == 'n':
            is_data_good = True
        else:
            error = 'Invalid response, please enter "Y" or "N"'
    display_data(districts)
    return districts


def get_total_number_of_votes():
    is_valid_votes = False
    while not is_valid_votes:
        votes = input("Please enter total number of votes: ")
        if votes.isnumeric() and '.' not in votes:
            is_valid_votes = True
        else:
            print(
                '"' + votes + '" is not a valid number. Please enter a positive whole number.')
    return int(votes)


def generate_table_data(districts, votes, key_len, bpi):
    total_population = sum(districts)
    table_data = []
    for count, population in enumerate(districts, start=1):
        if key_len > 3:
            table_data.append([count, population, population/total_population])
            table_data[count-1].append(int(table_data[count-1][2]*votes))
        if key_len > 4:
            table_data[count-1].append(bpi[count-1] - table_data[count-1][2])
    return table_data


def generate_table(districts, votes, key, bpi):
    table_data = generate_table_data(districts, votes, len(key), bpi)
    print(table_data)
    print_data = []
    for data in table_data:
        print_data.append(data.copy())
    # print(table_data)

    max_lengths = [0]*len(key)
    for count, data in enumerate(print_data):
        for index in range(len(data)):
            value = data[index]
            if index in [2, 4]:
                value = format_percentage(float(value))
            max_lengths[index] = max(max_lengths[index], len(str(value)))
            print_data[count][index] = str(value)
    for index, length in enumerate(max_lengths):
        max_lengths[index] = max(length, len(key[index]))
    print(max_lengths)
    # for data in print_data:
    #     print(data)
    # f'{"peter":{filler}<{width}}'
    for length in max_lengths:
        print(f'+-{"":-<{length}}-', end='')
    print('+')

    for index in range(len(key)):
        print(f'| {key[index]:<{max_lengths[index]}} ', end='')
    print('|')
    for length in max_lengths:
        print(f'+-{"":-<{length}}-', end='')
    print('+')

    for data in print_data:
        for data_index in range(len(data)):
            print(f'| {data[data_index]:<{max_lengths[data_index]}} ', end='')
        print('|')
    for length in max_lengths:
        print(f'+-{"":-<{length}}-', end='')
    print('+')

    return table_data


def format_percentage(value):
    # 0.1 -> 10.00%
    # 1.0 -> 100.00%
    # 0.01 -> 1.00%
    # 0.01345 -> 1.35%
    value = str(round(value*100, 2))
    if '.' in value:
        if len(value.split('.')[1]) < 2:
            value += '0'
    else:
        value += '.00'
    return value + '%'


def display_data(districts):
    # Counts the number of digits in the number of districts
    # If there are 1000 districts: len("1000") = 4
    district_number = len(str(len(districts)))

    # print(district_number)

    print_str = 'District' + ' '*(district_number+3) + '| Population'

    print(print_str)
    print('-' * (11 + district_number) + '+' + '-' * 12)

    # print("District".ljust(district_number + 3) + "Population")
    for district, population in enumerate(districts, start=1):
        print("District " + str(district).rjust(district_number) +
              ": | " + str(population))


main()

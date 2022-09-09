
# Pop. Prop. # incorrect percentage


def main():
    districts = input_data()
    votes = get_total_number_of_votes()
    # districts = [10, 20, 30, 40, 50]
    # votes = 150
    generate_table(districts, votes)


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


def generate_table(districts, votes):
    total_population = sum(districts)
    table_data = []
    for count, population in enumerate(districts, start=1):
        table_data.append([count, population, round(
            population/total_population, 2)])
        table_data[count-1].append(int(table_data[count-1][2]*votes))
    # for data in table_data:
    #     print(data)
    print_data = table_data.copy()
    key = ['District', 'Population', 'Pop. Proportion', '# Votes / Member']
    max_lengths = [0]*len(table_data[0])
    for count, data in enumerate(table_data):
        for index in range(len(data)):
            value = data[index]
            if index == 2:
                if len(str(value)) < 4:
                    value = str(value) + '0'
                value = str(value) + '%'
            max_lengths[index] = max(max_lengths[index], len(str(value)))
            print_data[count][index] = str(value)
    for index, length in enumerate(max_lengths):
        max_lengths[index] = max(length, len(key[index]))
    # print(max_lengths)
    # for data in print_data:
    #     print(data)

    # f'{"peter":{filler}<{width}}'
    print(
        f'+-{"":-<{max_lengths[0]}}-+-{"":-<{max_lengths[1]}}-+-{"":-<{max_lengths[2]}}-+-{"":-<{max_lengths[3]}}-+')
    print(f'| {key[0]:<{max_lengths[0]}} | {key[1]:<{max_lengths[1]}} | {key[2]:<{max_lengths[2]}} | {key[3]:<{max_lengths[3]}} |')
    print(
        f'+-{"":-<{max_lengths[0]}}-+-{"":-<{max_lengths[1]}}-+-{"":-<{max_lengths[2]}}-+-{"":-<{max_lengths[3]}}-+')

    for data in print_data:
        print(f'| {data[0]:<{max_lengths[0]}} | {data[1]:<{max_lengths[1]}} | {data[2]:<{max_lengths[2]}} | {data[3]:<{max_lengths[3]}} |')
    print(
        f'+-{"":-<{max_lengths[0]}}-+-{"":-<{max_lengths[1]}}-+-{"":-<{max_lengths[2]}}-+-{"":-<{max_lengths[3]}}-+')


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

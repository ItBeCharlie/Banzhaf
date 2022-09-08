
def main():
    # districts = input_data()
    get_total_number_of_votes()


def input_data():
    districts = []
    is_number_good = False
    while not is_number_good:
        response = input('Enter number of districts: ')
        try:
            district_number = int(response)
            districts = [0] * district_number
            is_number_good = True
        except:
            print('Please enter a positive whole number for number of districts "' + str(
                response) + '" is invalid.')
    current_district_index = 0
    current_district = current_district_index + 1

    while current_district_index < len(districts):
        response = input('Enter population of District ' +
                         str(current_district) + ": ")
        try:
            population = int(response)
            districts[current_district_index] = population
            current_district_index += 1
            current_district = current_district_index + 1
        except:
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
                try:
                    district_index = int(response) - 1
                    if district_index >= len(districts) or district_index < 0:
                        raise Exception()
                    is_population_fixed = False
                    while not is_population_fixed:
                        new_population = input(
                            "Please enter the new population for district " + str(response) + ": ")
                        try:
                            districts[district_index] = int(new_population)
                            is_population_fixed = True
                            is_district_fixed = True
                        except:
                            print('Please enter a positive whole number for population of district ' + str(response) + ', "' + str(
                                new_population) + '" is invalid.')
                except:
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


def display_data(districts):
    # Counts the number of digits in the number of districts
    # If there are 1000 districts: len("1000") = 4
    district_number = len(str(len(districts)))

    print(district_number)

    print_str = 'District' + ' '*(district_number+3) + '| Population'

    print(print_str)
    print('-' * (11 + district_number) + '+' + '-' * 12)

    # print("District".ljust(district_number + 3) + "Population")
    for district, population in enumerate(districts, start=1):
        print("District " + str(district).rjust(district_number) +
              ": | " + str(population))


main()

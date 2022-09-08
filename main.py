# Users will enter districts, populations, and number of board members
# Data structure:
# dictionary {district: {name: string, members: int, population: int}}

from dis import dis


districts = {}


def main():
    global districts
    print('You will be prompted below for district information, such as "District Name", "Number of Members", and "Population of District"')
    enter_information = True
    while enter_information:
        is_correct_name = False
        print('When you are done entering district information, enter "quit"')
        while not is_correct_name:
            district_name = input(
                'Please enter the name of the given district: ')
            if district_name.lower() == 'quit':
                enter_information = False
                break
            if approve_district_name(district_name):
                is_correct_name = True
                districts[district_name.lower()] = {
                    'name': district_name, 'members': None, 'population': None}
        is_correct_members = False
        if not enter_information:
            break
        while not is_correct_members:
            response = input(
                'Please enter the number of board members in ' + str(district_name) + ': ')
            try:
                board_members = int(response)
                if approve_board_members(board_members, district_name):
                    is_correct_members = True
                    districts[district_name.lower()]['members'] = board_members
            except:
                print('Please enter a positive whole number for number of board members, "' + str(
                    response) + '" is invalid.')
        is_correct_population = False
        while not is_correct_population:
            response = input(
                'Please enter the population in ' + str(district_name) + ': ')
            try:
                population = int(response)
                if approve_population(population, district_name):
                    is_correct_population = True
                    districts[district_name.lower()]['population'] = population
            except:
                print('Please enter a positive whole number for population, "' + str(
                    response) + '" is invalid.')
    display_district_information()


def display_district_information():
    for district in districts:
        print('District Name: ' + str(districts[district]['name']), 'Board Members: ' +
              str(districts[district]['members']), 'Population:    ' + str(districts[district]['population']), sep='\n', end='\n\n')


def approve_population(population, district_name):
    invalid_response = True
    while invalid_response:
        confirmation = input('Is "' + str(population) + '" the correct population for '
                             + str(district_name) + '? (Y/N): ').lower()
        if confirmation == 'y':
            is_correct_number = True
            invalid_response = False
        elif confirmation == 'n':
            is_correct_number = False
            invalid_response = False
        else:
            print('Invalid response, please enter "Y" or "N"')
    return is_correct_number


def approve_board_members(board_members, district_name):
    invalid_response = True
    while invalid_response:
        confirmation = input('Is "' + str(board_members) + '" the correct number of board members for '
                             + str(district_name) + '? (Y/N): ').lower()
        if confirmation == 'y':
            is_correct_number = True
            invalid_response = False
        elif confirmation == 'n':
            is_correct_number = False
            invalid_response = False
        else:
            print('Invalid response, please enter "Y" or "N"')
    return is_correct_number


def approve_district_name(district_name):
    invalid_response = True
    while invalid_response:
        confirmation = input('Is "' + district_name +
                             '" the correct district name? (Y/N): ').lower()
        if confirmation == 'y':
            is_correct_name = True
            invalid_response = False
        elif confirmation == 'n':
            is_correct_name = False
            invalid_response = False
        else:
            print('Invalid response, please enter "Y" or "N"')
    return is_correct_name


main()

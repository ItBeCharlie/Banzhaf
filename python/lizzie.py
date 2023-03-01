from main import run_program as calc
from bpi_new import calc_bpi
from District import District


def main():
    print('1: BPI Calculator')
    print('2: Weighed Vote Optimizer')
    mode = int(input('Select Mode: '))
    if mode not in [1, 2]:
        print('Error: Invalid Mode')
        exit()
    file = input('Enter csv file: ')
    with open(file) as f:
        lines = f.readlines()
    str_data = lines[0].strip().split(',')
    data = []
    for dat in str_data:
        data.append(int(dat))

    if mode == 1:
        result = calc_bpi(data)
        nice_print(result)

    elif mode == 2:
        votes = 100
        districts = []
        for index, population in enumerate(data):
            district = District(index)
            district.population = int(population)
            districts.append(district)
        calc(districts, votes)


def nice_print(data):
    max_len = len(str(len(data)))
    max_per_len = 9

    row_seperator = ('+' + '-'*(max_len+2) + '+' + '-'*(max_per_len+2)) + '+'

    print(row_seperator)
    for index, item in enumerate(data, start=1):
        print(f'| {index:>{max_len}} ', end='')
        print(f'| {f"{item:{max_per_len},.5%}":^5} ', end='')
        print('|')
        if index % 5 == 0:
            print(row_seperator)
    if len(data) % 5 != 0:
        print(row_seperator)


main()

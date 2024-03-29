# from bpi_old import calc_bpi_single
from bpi import calc_bpi

# Checks if an input is an integer


def is_int(val):
    val = str(val)
    if val.isnumeric() and '.' not in val:
        return True
    print(f'"{val}" is an invalid response. Please enter a positive whole number.')
    return False


def format_percentage(value, decimals=2):
    # 0.1 -> 10.00%
    # 1.0 -> 100.00%
    # 0.01 -> 1.00%
    # 0.01345 -> 1.35%
    value = str(round(value*100, decimals))
    if '.' in value:
        while len(value.split('.')[1]) < decimals:
            value += '0'
    else:
        value += '.' + '0'*decimals
    return value + '%'


def generate_bpi_data_old(districts):
    sum = 0
    bpi_data = [None] * len(districts)

    for district in districts:
        sum += district.votes_per_member
        bpi_data[district.number - 1] = district.votes_per_member
        # print(district.number, sum)

    bpi_data.insert(0, sum//2)
    bpi = calc_bpi(bpi_data)
    for index, district in enumerate(districts):
        district.bpi = bpi[index]

    return districts


def generate_bpi_data(district_set, quota):
    districts = district_set.districts
    bpi_data = [None] * len(districts)

    for district in districts:
        bpi_data[district.number-1] = int(district.votes_per_member)
        # print(district.number, sum)

    bpi_data.insert(0, quota)
    # print(bpi_data)
    bpi = calc_bpi(bpi_data)
    for index, district in enumerate(districts):
        district.bpi = bpi[index]


def display_table(districts, keys):
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

    # print(max_lengths)

    separator_string = ''

    for key in max_lengths:
        separator_string += f'+-{"":-<{max_lengths[key]}}-'
    separator_string += '+'
    print(separator_string)

    for key in keys:
        print(f'| {key:<{max_lengths[key]}} ', end='')
    print('|')

    print(separator_string)

    for row, data in enumerate(print_data, start=1):
        for key in keys:
            print(f'| {data[key]:<{max_lengths[key]}} ', end='')
        print('|')
        if row % 5 == 0 and row < len(print_data):
            print(separator_string)

    print(separator_string, end='\n\n')

    return table_data


def generate_data(districts, votes=None, keys=[]):
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

    return districts


def franklin_deviation(districts):
    min_score = 999999
    max_score = 0
    for district in districts:
        min_score = min(min_score, district.norm_bpi)
        max_score = max(max_score, district.norm_bpi)
    return max_score - min_score


def copy_iter_districts(iter_districts):
    new_iter_districts = []
    for district in iter_districts:
        new_iter_districts.append(district.clone())
    return new_iter_districts


def update_log(key, value, form='replace', type='str'):
    with open('log.csv') as f:
        lines = f.readlines()
        f.close()
    data = {}
    for line in lines:
        line = line.removesuffix('\n')
        if line == '':
            continue
        if line.split(',')[0] == key:
            if type == 'str':
                data[key] = line.split(',')[1]
            elif type == 'int':
                data[key] = int(line.split(',')[1])
            elif type == 'float':
                data[key] = float(line.split(',')[1])
        else:
            data[line.split(',')[0]] = line.split(',')[1]

    if form == 'replace':
        data[key] = value
    elif form == 'add':
        data[key] = data[key] + value

    with open('log.csv', 'w') as f:
        for d in data:
            f.write(f'{d},{data[d]}\n')
        f.close()


def get_log(key):
    with open('log.csv') as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        line = line.removesuffix('\n')
        if line == '':
            continue
        if line.split(',')[0] == key:
            return line.split(',')[1]

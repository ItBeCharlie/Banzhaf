from District import District
from helper import generate_bpi_data
from helper import display_table
from helper import generate_data


def iterate(districts):
    district_and_norm_bpi = build_district_tuples(districts.copy())
    # print(district_and_norm_bpi)
    district_and_norm_bpi_sorted = sort_district_list(
        district_and_norm_bpi.copy())
    # print(district_and_norm_bpi)

    max_iterations = 70
    cur_iteration = 0
    while cur_iteration < max_iterations:
        district_and_norm_bpi_sorted = sort_district_list(
            district_and_norm_bpi.copy())
        # for d in district_and_norm_bpi_sorted:
        #     print(d[1], end=' ')
        # print()
        min_norm_bpi_district = district_and_norm_bpi_sorted[0][0]
        max_norm_bpi_district = district_and_norm_bpi_sorted[-1][0]

        # print('Min: ', str(min_norm_bpi_district.number),
        #       str(min_norm_bpi_district.norm_bpi))
        # print('Max: ', str(max_norm_bpi_district.number),
        #       str(max_norm_bpi_district.norm_bpi))

        max_norm_bpi_district.votes_per_member -= 1
        min_norm_bpi_district.votes_per_member += 1

        new_districts = generate_bpi_data(
            reorder_district_list(district_and_norm_bpi))
        new_districts = generate_data(
            new_districts, keys=['Normalized BPI Score'])
        district_and_norm_bpi = build_district_tuples(new_districts.copy())
        district_and_norm_bpi_sorted = sort_district_list(
            district_and_norm_bpi.copy())

        cur_iteration += 1

        display_table(reorder_district_list(district_and_norm_bpi_sorted), ['District', 'Population', 'Pop. Proportion',
                                                                            '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    return reorder_district_list(district_and_norm_bpi_sorted)


def build_district_tuples(districts):
    district_and_norm_bpi = []
    for district in districts:
        district_and_norm_bpi.append((district, district.norm_bpi))
    return district_and_norm_bpi


def sort_district_list(list):
    list = list.copy()
    for i in range(len(list)):
        for j in range(len(list)-1):
            if list[j][1] > list[j+1][1]:
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp
            # print(list)
    return list


def reorder_district_list(list):
    list = list.copy()
    for i in range(len(list)):
        for j in range(len(list)-1):
            if list[j][0].number > list[j+1][0].number:
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp
    new_list = []
    for element in list:
        new_list.append(element[0])
    return new_list

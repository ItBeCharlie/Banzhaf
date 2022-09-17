from District import District
from helper import generate_bpi_data
from helper import display_table
from helper import generate_data
import copy


class IterDistrict:
    def __init__(self, district):
        self.district = district

    def update_info(self, district):
        self.district = copy.deepcopy(district)

    def compare_to(self, other_district, key='norm_bpi'):
        match key:
            case 'norm_bpi':
                return self.get_norm() - other_district.get_norm()
            case 'number':
                return self.district.number - other_district.district.number

    def get_norm(self):
        return self.district.norm_bpi


def iterate(districts):
    clean_districts = copy.deepcopy(districts)
    iter_districts = []
    for district in clean_districts:
        iter_districts.append(IterDistrict(district))

    # iter_districts_sorted = sort_iter_districts(iter_districts)

    max_iterations = 70
    cur_iteration = 0
    while cur_iteration < max_iterations:
        sort_iter_districts(iter_districts)

        # for d in district_and_norm_bpi_sorted:
        #     print(d[1], end=' ')
        # print()

        min_norm_bpi_iter_district = iter_districts[0]
        max_norm_bpi_iter_district = iter_districts[-1]

        # print('Min: ', str(min_norm_bpi_district.number),
        #       str(min_norm_bpi_district.norm_bpi))
        # print('Max: ', str(max_norm_bpi_district.number),
        #       str(max_norm_bpi_district.norm_bpi))

        min_norm_bpi_iter_district.district.votes_per_member -= 1
        max_norm_bpi_iter_district.district.votes_per_member += 1

        reorder_iter_district_list(iter_districts)

        normal_districts = iter_to_normal_districts(iter_districts)

        new_districts = generate_bpi_data(normal_districts)
        new_districts = generate_data(
            new_districts, keys=['Normalized BPI Score'])

        iter_districts = []
        for district in new_districts:
            iter_districts.append(IterDistrict(district))

        cur_iteration += 1
        reorder_iter_district_list(iter_districts)
        display_table(iter_to_normal_districts(iter_districts), ['District', 'Population', 'Pop. Proportion',
                                                                 '# Votes / Member', 'BPI Score', 'Normalized BPI Score'])

    return iter_to_normal_districts(iter_districts)


def sort_iter_districts(districts):
    districts.sort(key=lambda x: x.district.norm_bpi, reverse=True)


# def sort_iter_districts_old(districts):
#     for i in range(len(districts)):
#         for j in range(len(districts)-i-1):
#             if districts[j].compare_to(districts[j+1]) < 0:
#                 districts[j], districts[j+1] = districts[j+1], districts[j]


def reorder_iter_district_list(districts):
    districts.sort(key=lambda x: x.district.number, reverse=False)


# def reorder_iter_district_list_old(districts):
#     for i in range(len(districts)):
#         for j in range(len(districts)-i-1):
#             if districts[j].compare_to(districts[j+1], key='number') > 0:
#                 districts[j], districts[j+1] = districts[j+1], districts[j]


def iter_to_normal_districts(iter_districts):
    districts = []
    for district in iter_districts:
        districts.append(district.district)
    return districts

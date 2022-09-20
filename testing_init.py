from District import District


def init():
    districts = []
    for i in range(1, 11):
        districts.append(District(i))
    districts[0].population = 5671
    districts[1].population = 5671
    districts[2].population = 6237
    districts[3].population = 3924
    districts[4].population = 3745
    districts[5].population = 3227
    districts[6].population = 4044
    districts[7].population = 4057
    districts[8].population = 6632
    districts[9].population = 2628

    return districts, 10000

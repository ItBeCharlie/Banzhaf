from District import District


def init(case):
    districts = []
    if case == 1:
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
    elif case == 2:
        for i in range(1, 5):
            districts.append(District(i))
        districts[0].population = 150
        districts[1].population = 200
        districts[2].population = 250
        districts[3].population = 300
        return districts, 500
    elif case == 3:
        for i in range(1, 18):
            districts.append(District(i))
        districts[0].population = 7146
        districts[1].population = 4255
        districts[2].population = 2475
        districts[3].population = 8031
        districts[4].population = 3293
        districts[5].population = 2200
        districts[6].population = 4261
        districts[7].population = 7799
        districts[8].population = 4451
        districts[9].population = 5531
        districts[10].population = 3052
        districts[11].population = 787
        districts[12].population = 884
        districts[13].population = 1624
        districts[14].population = 2339
        districts[15].population = 1252
        districts[16].population = 3397
        return districts, 2009

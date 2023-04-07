from District import District
from DistrictSet import DistrictSet
import datetime


def main():
    time = datetime.datetime.now()
    time = time.strftime('%m-%d-%y-%H-%M-%S')

    print(time)
    district_set = test_read('case1.txt')
    
    


def test_read(file):
    global time  # TEMP
    with open(file) as f:
        lines = f.readlines()
    votes = int(lines[0])
    districts = []
    for i in range(1, len(lines)):
        districts.append(District(i-1))
        districts.population(int(lines[i]))

    return DistrictSet(districts, votes, time)


main()

# A place for me to test new python features I have never used


# print('Input test response: ', end='')
# print(input())

# print(input('Input test response: '))


from bpi_old import calc_bpi_single
from bpi_new import calc_bpi
from District import District

data = [137, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
districts = []
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


data = []
for i in districts:
    data.append(i.population)

data.insert(0, 10000)

q = data[0]

print(2**(len(data)-1), calc_bpi_single(data), sep='\n')
print()
print(((len(data)-1)**2) * q, calc_bpi(data), sep='\n')

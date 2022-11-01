from bpi_new import calc_bpi as cb
from bpi_old import calc_bpi_single


def calc_bpi(districts):
    # q = districts[0]
    # if 2**(len(districts)-1) < ((len(districts)-1)**2) * q:
    #     return calc_bpi_single(districts)
    return cb(districts)

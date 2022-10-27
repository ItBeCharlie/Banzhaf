from pretty_print import pretty_table as pt
import itertools


test = [6, 4, 3, 2, 1]


def calc_bpi(data):
    q = test[0]
    S = data[1:]

    # print(q, S)

    # x_names = []
    # for i in range(q):
    #     x_names.append(i)

    # y_names = []
    # for i in range(len(S) + 1):
    #     y_names.append(f'p{i}')

    # print(x_names, y_names)

    build_f(q, S, 0)


def build_f(q, S, p):
    table = [[0]*q for i in range(len(S)+1)]
    table[0][0] = 1
    S[p], S[-1] = S[-1], S[p]
    print(S)
    for index in range(1, len(S)+1):
        for y in range(q):
            # table[index][y] = table[index-1][y]
            # if S[index-1] <= y:
            #     table[index][y] += table[index-1][y-S[index-1]]
            if S[index-1] <= y:
                table[index][y] = table[index-1][y] + \
                    table[index-1][y-S[index-1]]
            else:
                table[index][y] = table[index-1][y]
    print(table)


def f(p_iw, y):
    pass


calc_bpi(test)

# print(list(itertools.permutations([1, 2, 3])))

from pretty_print import pretty_table as pt
import itertools


test = [6, 4, 3, 2, 1]
nassau = [16, 9, 9, 7, 3, 1, 1]
usec = [61, 55, 38, 29]


def calc_bpi(data):
    q = data[0]
    S = data[1:]

    print(q, S)

    scores = []

    for index, p in enumerate(S, start=1):
        f = build_f(q, S.copy(), index)
        w_sum = 0
        for y in range(q-p, q):
            w_sum += f[-2][y]
        print(w_sum)
        scores.append(w_sum)
    print(scores)


def build_f(q, S, p_i):
    player_labels = [f'p{i}' for i in range(len(S)+1)]

    table = [[0]*q for i in range(len(S)+1)]
    table[0][0] = 1

    S[p_i-1], S[-1] = S[-1], S[p_i-1]
    player_labels[p_i], player_labels[-1] = player_labels[-1], player_labels[p_i]
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

    pt(table=table, y_names=player_labels, key=player_labels[-1])
    return table


calc_bpi(test)

# print(list(itertools.permutations([1, 2, 3])))

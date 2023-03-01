from pretty_print import pretty_table as pt
from multiprocessing import Pool
import itertools


test = [6, 4, 3, 2, 1]
nassau = [16, 9, 9, 7, 3, 1, 1]
usec = [61, 55, 38, 29]
lizzie = [2400, 130, 63, 208, 297, 512, 171, 241, 132,
          322, 158, 168, 132, 153, 375, 250, 577, 277, 125, 558]
lizzie2 = [4260//2 + 1, 275, 148, 48, 172, 273, 448,
           474, 356, 69, 166, 137, 132, 780, 45, 199, 244, 294]


def calc_bpi(data):
    return calc_bpi_single_thread(data)


def calc_bpi_single_thread(data):
    q = data[0]
    S = data[1:]

    # print(q, S)

    scores = []

    for index, p in enumerate(S, start=1):
        f = build_f(q, S.copy(), index)
        w_sum = 0
        for y in range(q-p, q):
            w_sum += f[-2][y]
        # print(w_sum)
        scores.append(w_sum)
    # print(scores)
    return normalize_score(scores)


def calc_bpi_multi_thread(data):
    q = data[0]
    S = data[1:]

    # print(q, S)

    info = []

    for index, p in enumerate(S, start=1):
        info.append([q, S.copy(), index, p])

    # for item in info:
    #     print(item)

    scores = []
    results = []
    pool = Pool()
    results = list(pool.imap(thread_p, info))
    print('ERR1')

    print(results)
    print('ERR2')
    c = 0

    for result in results:
        print(f'ERR3 {c}')
        c += 1
        scores.append(result.get())
        print('ERR4')
    print('ERR5')

    print(scores)

    return normalize_score(scores)


def thread_p(inp: list):
    print('hello')
    q = inp[0]
    S = inp[1]
    index = inp[2]
    p = inp[3]

    print(q)
    f = build_f(q, S.copy(), index)
    w_sum = 0
    for y in range(q-p, q):
        w_sum += f[-2][y]
    print(w_sum)
    return w_sum


def normalize_score(scores):
    score_sum = sum(scores)
    if score_sum == 0:
        return scores
    normalized_scores = []
    for score in scores:
        normalized_scores.append(score / score_sum)
    return normalized_scores


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

    # pt(table=table, y_names=player_labels, key=player_labels[-1])
    return table


# liz = calc_bpi(lizzie2)

# for element in liz:
#     print(f'{int(element*1000)/10}%')


# print(list(itertools.permutations([1, 2, 3])))

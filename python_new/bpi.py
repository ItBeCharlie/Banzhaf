from pretty_print import pretty_table as pt

test = [6, 4, 3, 2, 1]


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


print(calc_bpi(test))

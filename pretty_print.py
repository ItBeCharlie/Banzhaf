
x_names = [0, 1, 2, 3, 4, 5]
y_names = ['p0', 'p1', 'p2', 'p3', 'p4']

table = [[1, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1, 0],
         [1, 0, 0, 1, 1, 0],
         [1, 0, 1, 1, 1, 1],
         [1, 1, 1, 2, 2, 2]]

key = 'p\\y'


def pretty_table(x_names, y_names, table, key):
    str_table = []
    x_names, max_x = to_str_list(x_names)
    y_names, max_y = to_str_list(y_names)
    max_len = max(max_x, max_y, len(key))
    for row in table:
        result, cur_max = to_str_list(row)
        str_table.append(result)
        max_len = max(max_len, cur_max)

    table = str_table

    row_seperator = ('+' + '-'*(max_len+2))*(len(table[0])+1) + '+'

    print(row_seperator)

    print(f'| {key:^{max_len}} ', end='')
    for item in x_names:
        print(f'| {item:^{max_len}} ', end='')
    print('|')
    print(row_seperator)
    for index, row in enumerate(table):
        print(f'| {y_names[index]:>{max_len}} ', end='')
        for item in row:
            print(f'| {item:^{max_len}} ', end='')
        print('|')
        print(row_seperator)


def to_str_list(list):
    max_len = 0
    new_list = []
    for item in list:
        new_list.append(str(item))
        max_len = max(max_len, len(str(item)))
    return new_list, max_len


pretty_table(x_names, y_names, table, key)

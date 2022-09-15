# Checks if an input is an integer
def is_int(val):
    val = str(val)
    if val.isnumeric() and '.' not in val:
        return True
    print(f'"{val}" is an invalid response. Please enter a positive whole number.')
    return False


def format_percentage(value):
    # 0.1 -> 10.00%
    # 1.0 -> 100.00%
    # 0.01 -> 1.00%
    # 0.01345 -> 1.35%
    value = str(round(value*100, 2))
    if '.' in value:
        if len(value.split('.')[1]) < 2:
            value += '0'
    else:
        value += '.00'
    return value + '%'

INPUT_ERROR_INT = 'Must be an integer. Try again.'
INPUT_ERROR_STR = 'Must be either K, C, R, F. Try again.'

# Input validation
def input_num(message):
    while True:
        try:
            user_input = int(input(message))
        except ValueError:
            print(INPUT_ERROR_INT)
            continue
        else:
            return user_input
            break


def input_str(message):
    while True:
        try:
            user_input = str(input(message).upper())
            if user_input not in ['K', 'C', 'R', 'F']:
                raise ValueError
        except ValueError:
            print(INPUT_ERROR_STR)
            continue
        else:
            return user_input
            break

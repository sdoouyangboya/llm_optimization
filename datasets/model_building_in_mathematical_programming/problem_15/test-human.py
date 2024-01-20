import json

eps = 1e-03


def run():

    error_list = []

    with open('data.json', 'r') as f:
        data = json.load(f)

    try:
        with open('output.json', 'r') as f:
            output = json.load(f)
    except FileNotFoundError:
        error_list.append("Some constraints are missing and the problem is unbounded! Please double check")

    if not "quadratic" in output:
        error_list.append("The output field 'quadratic' is missing")

    if not "linear" in output:
        error_list.append("The output field 'linear' is missing")

    if not "constant" in output:
        error_list.append("The output field 'constant' is missing")


    return error_list



if __name__ == '__main__':
    run()
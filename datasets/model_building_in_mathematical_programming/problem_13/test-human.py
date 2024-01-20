import json

eps = 1e-03

"""
This is acturally an unconstrained problem

"""


def run():

    error_list = []

    with open('data.json', 'r') as f:
        data = json.load(f)

    try:
        with open('output.json', 'r') as f:
            output = json.load(f)
    except FileNotFoundError:
        error_list.append("Some constraints are missing and the problem is unbounded! Please double check")

    if not "intercept" in output:
        error_list.append("The output field 'intercept' is missing")

    if not "slope" in output:
        error_list.append("The output field 'slope' is missing")


    return error_list



if __name__ == '__main__':
    run()
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

    if "isincluded" not in output:
        error_list.append("Missing isincluded in output!")

    n_items = len(data["value"])

    total_size = 0

    # Check if the knapsack constraint is violated
    for i in range(n_items):
        total_size += data["size"][i] * output["isincluded"][i]

    if total_size >= data["C"] + eps:
        error_list.append("The size %f is exceeded by %f" % (data["C"], total_size))

    return error_list


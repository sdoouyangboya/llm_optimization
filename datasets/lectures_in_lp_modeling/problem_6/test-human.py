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

    if "quantity" not in output:
        error_list.append("Missing quantity in output!")

    n_parts = len(data["time"])
    n_shops = len(data["capacity"])

    total_profit = 0.0

    for k in range(n_shops):
        work_hours = 0.0
        for i in range(n_parts):
            work_hours += output["quantity"][i] * data["time"][i][k]
        if work_hours > data["capacity"][k]:
            error_list.append(f"The capacity of shop %d is %f. But the working hours is %f " % \
                   (k + 1, data["capacity"][k], work_hours))

    for i in range(n_parts):
        total_profit += output["quantity"][i] * data["profit"][i]

    return error_list

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

    n_products = len(data["produce_time"])
    n_stages = len(data["available_time"])

    for k in range(n_products):
        if output["quantity"][k] < -eps:
            error_list.append("Quantity of product %d must be non-negative" % (k + 1))

    for s in range(n_stages):
        time_spent = 0.0
        for k in range(n_products):
            time_spent += data["produce_time"][k][s]
        if time_spent >= data["available_time"][s] + eps:
            error_list.append("Not enough available time for stage %d. We have limit %f but the current value is %f" % \
                   (s + 1, data["available_time"], time_spent))

    return error_list


if __name__ == '__main__':
    run()

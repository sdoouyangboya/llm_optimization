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

    n_nutrition = len(data["demand"])
    n_food = len(data["price"])

    # Check whether all the demands are fulfilled
    for i in range(n_nutrition):
        n_satisfied_nutrition = 0
        for k in range(n_food):
            n_satisfied_nutrition += data["nutrition"][k][i] * output["quantity"][k]

        if n_satisfied_nutrition < data["demand"][i] - eps:
            error_list.append(f"Nutrition %d should be at least %f units but only %f is fulfilled" % \
                   (i + 1, data["demand"][i], n_satisfied_nutrition))

    return error_list

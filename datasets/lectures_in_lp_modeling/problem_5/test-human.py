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

    if "amount" not in output:
        error_list.append("Missing amount in output!")

    n_metal = len(data["target"])
    n_alloy = len(data["price"])

    total_cost = 0.0

    # Check if the ratio satisfies the target
    for i in range(n_metal):
        metal_quantity = 0.0
        for k in range(n_alloy):
            metal_quantity += output["amount"][k] * data["ratio"][k][i]
        if abs(metal_quantity - data["target"][i]) > eps:
            error_list.append(f"We need %f of metal %d but we get %f. " % (data["target"][i] * data["alloy_quant"], i + 1, metal_quantity))
            error_list.append(f"Check if this is because something wrong with percentage conversion")

    # Sum over the cost
    for i in range(n_alloy):
        total_cost += output["amount"][i] * data["price"][i]

    return error_list

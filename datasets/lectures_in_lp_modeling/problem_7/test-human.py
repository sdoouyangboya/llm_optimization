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

    if "reg_quant" not in output:
        error_list.append("Missing reg_quant in output!")

    if "over_quant" not in output:
        error_list.append("Missing over_quant in output!")

    n_month = len(data["demand"])

    stock = 0.0
    total_cost = 0.0

    for i in range(n_month):
        
        stock = stock + output["reg_quant"][i] + output["over_quant"][i] - data["demand"][i]
        total_cost += output["reg_quant"][i] * data["cost_regular"] + output["over_quant"][i] * data["cost_overtime"]
        if stock < 0.0:
            error_list.append("The production quantity for month %d does not meet the demand" % (i + 1))

        total_cost += stock * data["store_cost"]

    return error_list

if __name__ == '__main__':
    run()
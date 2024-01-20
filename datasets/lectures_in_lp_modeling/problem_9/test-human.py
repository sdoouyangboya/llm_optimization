import json

eps = 1e-03


def run():

    err_list = []

    with open('data.json', 'r') as f:
        data = json.load(f)

    try:
        with open('output.json', 'r') as f:
            output = json.load(f)
    except FileNotFoundError:
        err_list.append("Some constraints are missing and the problem is unbounded! Please double check")

    if "amount" not in output:
        err_list.append("Missing amount in output!")

    n_mineral = len(data["contsi"])

    # Check Mn percentage
    percent_mn = 0.0
    for i in range(n_mineral):
        percent_mn += data["contmn"][i] * output["amount"][i] + output["num_mang"]

    percent_mn = percent_mn / (sum(output["amount"]) + output["num_mang"])

    if sum(output["amount"]) + output["num_mang"] < data["n_steel_quant"]:
        err_list.append("The order cannot be filled")

    if percent_mn < data["mn_percent"] - eps :
        err_list.append("The required percentage of Mn is %f. But we get %f now" %
                        (data["mn_percent"], percent_mn))

    percent_si = 0.0
    for i in range(n_mineral):
        percent_si += data["contsi"][i] * output["amount"][i]

    percent_si = percent_si / sum(output["amount"])

    if percent_si >= data["si_max"]:
        err_list.append("The required percentage of Si is at most %f. But we get %f now" %
                        (data["si_max"], percent_si))

    if percent_si <= data["si_min"]:
        err_list.append("The required percentage of Si is at least %f. But we get %f now"
                        % (data["si_min"], percent_si))

    total_cost = 0.0

    for i in range(n_mineral):
        total_cost += output["amount"][i] * data["cost"][i]
        total_cost += output["amount"][i] * data["melt_price"]

    total_cost += output["num_mang"] * data["mang_price"]
    total_earn = data["n_steel_quant"] * data["sell_price"]

    return err_list

if __name__ == '__main__':
    print(run())

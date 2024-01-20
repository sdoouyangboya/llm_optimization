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
        error_list.append(f"Some constraints are missing and the problem is unbounded! Please double check")

    if "buyquantity" not in output:
        error_list.append(f"Missing buyquantity in output!")
    if "sellquantity" not in output:
        error_list.append(f"Missing sellquantity in output!")

    n_periods = len(data["price"])
    stock = 0.0
    total_cost = 0.0
    total_earn = 0.0

    for t in range(n_periods):
        
        if output["buyquantity"][t] < -eps:
            error_list.append(f"Quantity of buying in period %d is negative" % (t + 1))
        if output["sellquantity"][t] < -eps:
            error_list.append(f"Quantity of selling in period %d is negative" % (t + 1))

        total_cost += output["buyquantity"][t] * data["cost"][t]
        total_earn += output["sellquantity"][t] * data["price"][t]

        # Add the holding cost
        total_cost += output["stock"][t] * data["holding_cost"]

        if stock < -eps:
            error_list.append(f"The stock in hand at period %d is negative" % (t + 1))

        if stock > data["capacity"]:
            error_list.append(f"The stock at period %d exceeds the allowed capacity %d" % (t + 1, data["capacity"]))

    total_revenue = total_earn - total_cost
    if stock != 0.0:
        error_list.append(f"Warehouse should be empty at the end of the last period")

    return error_list


if __name__ == '__main__':
    run()
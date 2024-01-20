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

    if not "buy" in output:
        error_list.append("The output field 'buy' is missing")

    if not "refine" in output:
        error_list.append("The output field 'refine' is missing")

    if not "storage" in output:
        error_list.append("The output field 'storage' is missing")

    max_veg = data["max_vegetable_refining_per_month"]
    max_non_veg = data["max_non_vegetable_refining_per_month"]
    storage_size = data["storage_size"]
    init_amount = data["init_amount"]
    veg_oils = []
    non_veg_oils = []

    num_months = len(data["buy_price"])

    # Get vegetable and non vegetable oils
    for i in range(len(data["is_vegetable"])):
        if data["is_vegetable"][i]:
            veg_oils.append(i)
        else:
            non_veg_oils.append(i)

    veg_refined = []
    non_veg_refined = []

    # Get the sum quantity of two kinds of oils
    for m in range(num_months):
        veg_refined.append(sum([output["refine"][m][i] for i in veg_oils]))
        non_veg_refined.append(sum([output["refine"][m][i] for i in non_veg_oils]))

    # Check the limiting capacity
    for m in range(num_months):
        if veg_refined[m] > max_veg + eps:
            error_list.append(f"The refined quantity of vegetable oils in month {m + 1} exceeds the maximum refining capacity")
        if non_veg_refined[m] > max_non_veg + eps:
            error_list.append(f"The refined quantity of non-vegetable oils in month {m + 1} exceeds the maximum refining capacity")

    # Check the storage capacity
    for m in range(num_months):
        for i in range(len(data["buy_price"][0])):
            if output["storage"][m][i] >= storage_size + eps:
                error_list.append(f"Storage of oil {i + 1} in month {m + 1} exceeds the limit")

    # Assert the hardness is correct for the product
    for m in range(num_months):
        hardness = sum([output["refine"][m][i] * data["hardness"][i] for i in range(len(data["hardness"]))])
        hardness = hardness / sum([output["refine"][m][i] for i in range(len(data["hardness"]))])
        if hardness >= data["max_hardness"] + eps:
            error_list.append(f"Hardness of product in month {m + 1} is higher than the maximum limit")
        if hardness <= data["min_hardness"] - eps:
            error_list.append(f"Hardness of product in month {m + 1} is lower than the lower limit")

    # Ensure the storage is the same at the end
    for i in range(len(data["buy_price"][0])):
        if abs(output["storage"][-1][i] - data["init_amount"]) > eps:
            error_list.append("Storage of oil %d at the end is not equal to initial amount" % (i + 1)) 

    # Ensure that if an oil is used, it must be used for 20 tons
    for m in range(num_months):
        for i in range(len(data["is_vegetable"])):
            if output["refine"][m][i] > eps:
                if output["refine"][m][i] < data["min_usage"] - eps:
                    error_list.append("Oil %d is used in month %d but its usage is less than the minimum usage" % 
                        (i + 1, m + 1)) 

    # Ensure that at most three oils are used in each month
    for m in range(num_months):
        n_used_oils = 0
        
        for i in range(len(data["is_vegetable"])):
            if output["refine"][m][i] > eps:
                n_used_oils += 1
        
        if n_used_oils > 3:
            error_list.append("More than three kinds of oil are used in month %d" % (m + 1))

    # Ensure that dependency is respected 
    for m in range(num_months):
        for i in range(len(data["is_vegetable"])):
            if output["refine"][m][i] > eps:
                for j in range(len(data["is_vegetable"])):
                    if data["dependencies"][i][j] == 1 and output["refine"][m][j] < eps:
                        error_list.append("In month %d dependency is violated: oil %d is used but oil %d is not" % (m + 1, i + 1, j + 1))

    # Compute the total profit and cost
    total_profit = 0.0
    total_cost = 0.0

    for m in range(num_months):
        total_profit += sum([output["refine"][m][i] for i in range(len(data["hardness"]))]) * data["sell_price"]
        for i in range(len(data["buy_price"][0])):
            total_cost += data["buy_price"][m][i] * output["buy"][m][i]
            total_cost += data["storage_cost"] * output["storage"][m][i]

    total_revenue = total_profit - total_cost

    return error_list


if __name__ == '__main__':
    print(run())
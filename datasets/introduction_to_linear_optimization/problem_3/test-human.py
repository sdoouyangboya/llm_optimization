import json

eps = 1e-03


def run():
    with open("data.json", "r") as f:
        data = json.load(f)

    with open("output.json", "r") as f:
        output = json.load(f)

    error_list = []

    # Check if all the required keys are present in the output.
    for key in ["coal_cap_added", "nuke_cap_added", "total_cost"]:
        if key not in output:
            error_list.append(f"The output field '{key}' is missing")

    # Check if the total capacity (oil + coal + nuclear) is enough to meet the demand in each year.
    total_added_capacity = 0
    total_added_nuke_capacity = 0

    partial_sum_coal = [0] * len(data["demand"])
    partial_sum_nuke = [0] * len(data["demand"])

    for t in range(len(data["demand"])):
        for k in ["coal_cap_added", "nuke_cap_added"]:
            if output[k][t] < -eps:
                error_list.append(f"The {k} in year {t+1} is negative")
                return error_list

        partial_sum_coal[t] = output["coal_cap_added"][t] + (
            partial_sum_coal[t - 1] if t > 0 else 0
        )
        partial_sum_nuke[t] = output["nuke_cap_added"][t] + (
            partial_sum_nuke[t - 1] if t > 0 else 0
        )

    for t in range(len(data["demand"])):
        partial_sum_coal[t] -= (
            partial_sum_coal[t - data["coal_life"]] if t >= data["coal_life"] else 0
        )
        partial_sum_nuke[t] -= (
            partial_sum_nuke[t - data["nuke_life"]] if t >= data["nuke_life"] else 0
        )

    for t in range(len(data["demand"])):
        total_capacity = data["oil_cap"][t] + partial_sum_coal[t] + partial_sum_nuke[t]

        if total_capacity < data["demand"][t] - eps:
            error_list.append(
                f"The total capacity in year {t+1} is not enough to meet the demand"
            )
            return error_list

        if partial_sum_nuke[t] > data["max_nuke"] / 100.0 * total_capacity + eps:
            error_list.append(
                f"The nuclear capacity in year {t+1} exceeds the maximum allowed percentage"
            )
        print(total_capacity, data["demand"][t])

    # Check if the total cost is correctly calculated.
    total_cost = sum(
        data["coal_cost"] * output["coal_cap_added"][t]
        + data["nuke_cost"] * output["nuke_cap_added"][t]
        for t in range(len(data["demand"]))
    )

    if abs(total_cost - output["total_cost"]) > eps:
        error_list.append("The total cost is not correctly calculated")

    return error_list


if __name__ == "__main__":
    print(run())

import json

eps = 1e-03


def parse_json(json_file, keys):
    if isinstance(json_file, list):
        for v in json_file:
            parse_json(v, keys)
    elif isinstance(json_file, dict):
        for k, v in json_file.items():
            if isinstance(v, dict) or isinstance(v, list):
                parse_json(v, keys)
            if k not in keys:
                keys.append(k)


def run():
    with open("data.json", "r") as f:
        data = json.load(f)

    with open("output.json", "r") as f:
        output = json.load(f)

    all_json_keys = []
    parse_json(output, all_json_keys)

    error_list = []

    if not "net_income" in all_json_keys:
        error_list.append("The output field 'net_income' is missing")

    if not "production" in all_json_keys:
        error_list.append("The output field 'production' is missing")

    if not "upgrade" in all_json_keys:
        error_list.append("The output field 'upgrade' is missing")

    # Check if production quantities are non-negative
    for i, production_i in enumerate(output["production"]):
        if production_i < -eps:
            error_list.append(
                f"Production quantity of product {i+1} is negative: {production_i}"
            )

    # Check if machine hours do not exceed available hours
    total_hours = sum(
        production_i * hour_i
        for production_i, hour_i in zip(output["production"], data["hour"])
    )
    if output["upgrade"]:
        available_hours = data["availableHours"] + data["upgradeHours"]

    if total_hours - available_hours > eps:
        error_list.append(
            f"Total machine hours used ({total_hours}) exceed available hours ({data['availableHours']})"
        )

    # Check if total cost does not exceed available cash
    total_cost = sum(
        production_i * cost_i
        for production_i, cost_i in zip(output["production"], data["cost"])
    )

    if output["upgrade"]:
        total_cost += data["upgradeCost"]

    total_revenue = sum(
        production_i * price_i * (1 - investPercentage_i)
        for production_i, price_i, investPercentage_i in zip(
            output["production"], data["price"], data["investPercentage"]
        )
    )
    if total_cost - data["cash"] > eps:
        error_list.append(
            f"Total cost ({total_cost}) exceeds available cash ({data['cash']})"
        )

    # Check if net income is correctly calculated
    net_income = total_revenue - total_cost
    if abs(net_income - output["net_income"]) > eps:
        error_list.append(
            f"Net income is incorrectly calculated: expected {net_income}, got {output['net_income']}"
        )

    return error_list


if __name__ == "__main__":
    print(run())

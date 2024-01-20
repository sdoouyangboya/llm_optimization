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

    if not "dailyProfit" in all_json_keys:
        error_list.append("The output field 'dailyProfit' is missing")

    if not "unitsProduced" in all_json_keys:
        error_list.append("The output field 'unitsProduced' is missing")

    if not "overtimeAssembly" in all_json_keys:
        error_list.append("The output field 'overtimeAssembly' is missing")

    if not "materialBought" in all_json_keys:
        error_list.append("The output field 'materialBought' is missing")

    total_assembly = sum(
        [a * b for a, b in zip(data["assemblyHour"], output["unitsProduced"])]
    )

    if output["overtimeAssembly"] - data["maxOvertimeAssembly"] > eps:
        error_list.append(
            f"Total assembly hours ({output['overtimeAssembly']}) exceed the maximum assembly hours ({data['maxOvertimeAssembly']})"
        )

    if total_assembly > data["maxAssembly"] + output["overtimeAssembly"] + eps:
        error_list.append(
            f"Total assembly hours ({total_assembly}) exceed the maximum assembly hours ({data['maxAssembly']})"
        )

    total_testing = sum(
        [a * b for a, b in zip(data["testingHour"], output["unitsProduced"])]
    )
    if total_testing - data["maxTesting"] > eps:
        error_list.append(
            f"Total testing hours ({total_testing}) exceed the maximum testing hours ({data['maxTesting']})"
        )

    total_material_cost = sum(
        [a * b for a, b in zip(data["materialCost"], output["unitsProduced"])]
    )
    if abs(total_material_cost - output["materialBought"]) > eps:
        error_list.append(
            f"Total cost of raw materials ({total_material_cost}) is not consistent with the amount of raw materials bought ({output['materialBought']})"
        )

    overtime_cost = data["overtimeAssemblyCost"] * output["overtimeAssembly"]
    if (
        abs(overtime_cost - output["overtimeAssembly"] * data["overtimeAssemblyCost"])
        > eps
    ):
        error_list.append(
            f"Total cost of overtime assembly ({overtime_cost}) is not consistent with the overtime hours ({output['overtimeAssembly']})"
        )

    total_revenue = sum([a * b for a, b in zip(data["price"], output["unitsProduced"])])
    total_cost = total_material_cost + overtime_cost
    if total_material_cost > data["discountThreshold"]:
        total_cost *= 1 - data["materialDiscount"] / 100
    if abs(total_revenue - total_cost - output["dailyProfit"]) > eps:
        error_list.append(
            f"Daily profit ({output['dailyProfit']}) is not calculated correctly. It should be {total_revenue - total_cost}"
        )

    return error_list


if __name__ == "__main__":
    print(run())

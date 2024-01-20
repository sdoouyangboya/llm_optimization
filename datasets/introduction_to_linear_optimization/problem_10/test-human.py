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

    if not "x" in all_json_keys:
        error_list.append("The output field 'x' is missing")

    if not "cost" in all_json_keys:
        error_list.append("The output field 'cost' is missing")

    if "x" in all_json_keys:
        if len(output["x"]) != len(data["deliver"]):
            error_list.append(
                f"The length of the produced units array 'x' ({len(output['x'])}) does not match the length of the delivery array 'deliver' ({len(data['deliver'])})"
            )

        inventory = 0
        total_cost = 0
        for i in range(len(data["deliver"])):
            if output["x"][i] + inventory < data["deliver"][i] - eps:
                error_list.append(
                    f"In month {i+1}, the production ({output['x'][i]}) plus inventory ({inventory}) is less than the delivery ({data['deliver'][i]})"
                )
            inventory = output["x"][i] + inventory - data["deliver"][i]
            total_cost += inventory * data["storage_cost"]
            if i > 0:
                total_cost += data["switch_cost"] * abs(
                    output["x"][i] - output["x"][i - 1]
                )
        if abs(total_cost - output["cost"]) > eps:
            error_list.append(
                f"The total cost calculated in the output ({output['cost']}) does not match the actual total cost ({total_cost})"
            )

    return error_list


if __name__ == "__main__":
    print(run())

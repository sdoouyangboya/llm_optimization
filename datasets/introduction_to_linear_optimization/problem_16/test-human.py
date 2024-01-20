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

    if not "revenue" in all_json_keys:
        error_list.append("The output field 'revenue' is missing")

    if not "execute" in all_json_keys:
        error_list.append("The output field 'execute' is missing")

    # Problem specific testing code
    if "execute" in all_json_keys:
        if len(output["execute"]) != len(data["cost"]):
            error_list.append(
                "The length of 'execute' field does not match the number of processes"
            )

        if any(execute < -eps for execute in output["execute"]):
            error_list.append("The 'execute' field contains negative numbers")

        total_input = [
            sum(
                data["input"][l][i] * output["execute"][l]
                for l in range(len(data["input"]))
            )
            for i in range(len(data["allocated"]))
        ]

        for i, total in enumerate(total_input):
            if total - data["allocated"][i] > eps:
                error_list.append(
                    f"The total amount of crude oil type {i+1} used ({total}) exceeds the allocated amount ({data['allocated'][i]})"
                )

        calculated_revenue = sum(
            sum(
                data["output"][l][p] * data["price"][p] * output["execute"][l]
                for p in range(len(data["price"]))
            )
            for l in range(len(data["output"]))
        ) - sum(
            data["cost"][l] * output["execute"][l] for l in range(len(data["cost"]))
        )
        if abs(calculated_revenue - output["revenue"]) > eps:
            error_list.append(
                f"The calculated revenue ({calculated_revenue}) does not match the 'revenue' field in the output ({output['revenue']})"
            )

    return error_list


if __name__ == "__main__":
    print(run())

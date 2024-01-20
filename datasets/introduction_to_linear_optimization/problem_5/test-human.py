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

    # Check if all required keys are present
    required_keys = [
        "optimized_paths",
        "paths",
        "source",
        "destination",
        "route",
        "path_flow",
        "path_cost",
        "total_cost",
    ]
    for key in required_keys:
        if key not in all_json_keys:
            error_list.append(f"The output field '{key}' is missing")

    # Check if the total cost is the sum of all path costs
    total_cost = sum(path["path_cost"] for path in output["optimized_paths"]["paths"])
    if abs(total_cost - output["optimized_paths"]["total_cost"]) > eps:
        error_list.append("The total cost is not the sum of all path costs")

    # Check if the flow in each path does not exceed the capacity of the links
    for path in output["optimized_paths"]["paths"]:
        for i in range(len(path["route"]) - 1):
            link = next(
                (
                    link
                    for link in data["links"]
                    if link["start"] == path["route"][i]
                    and link["end"] == path["route"][i + 1]
                ),
                None,
            )
            if link and path["path_flow"] > link["U"] + eps:
                error_list.append(
                    f"The flow in path from {path['source']} to {path['destination']} exceeds the capacity of the link from {link['start']} to {link['end']}"
                )

    # Check if the total flow from each source to each destination is equal to the data rate
    for data_item in data["data"]:
        total_flow = sum(
            path["path_flow"]
            for path in output["optimized_paths"]["paths"]
            if path["source"] == data_item["source"]
            and path["destination"] == data_item["destination"]
        )
        if abs(total_flow - data_item["rate"]) > eps:
            error_list.append(
                f"The total flow from {data_item['source']} to {data_item['destination']} is not equal to the data rate"
            )

    # Check if the cost of each path is equal to the sum of the costs of the links in the path multiplied by the flow
    for path in output["optimized_paths"]["paths"]:
        path_cost = 0
        for i in range(len(path["route"]) - 1):
            link = next(
                (
                    link
                    for link in data["links"]
                    if link["start"] == path["route"][i]
                    and link["end"] == path["route"][i + 1]
                ),
                None,
            )
            if link:
                path_cost += link["C"] * path["path_flow"]
        if abs(path_cost - path["path_cost"]) > eps:
            error_list.append(
                f"The cost of path from {path['source']} to {path['destination']} is not equal to the sum of the costs of the links in the path multiplied by the flow"
            )

    return error_list


if __name__ == "__main__":
    print(run())

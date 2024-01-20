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

    if not "start" in all_json_keys:
        error_list.append("The output field 'start' is missing")

    if not "total" in all_json_keys:
        error_list.append("The output field 'total' is missing")

    if "start" in all_json_keys:
        if len(output["start"]) != 7:
            error_list.append(
                "The output field 'start' should contain exactly 7 elements"
            )

        if any(not isinstance(start, int) or start < -eps for start in output["start"]):
            error_list.append(
                "The output field 'start' should contain non-negative integers only"
            )

    if "total" in all_json_keys:
        if not isinstance(output["total"], int) or output["total"] < -eps:
            error_list.append(
                "The output field 'total' should be a non-negative integer"
            )

    if "start" in all_json_keys and "total" in all_json_keys:
        if abs(sum(output["start"]) - output["total"]) > eps:
            error_list.append(
                "The sum of the 'start' list should equal the 'total' value"
            )

    period = int(data["period"])
    demand = [int(d) for d in data["demand"]]

    for j in range(7):
        if sum(output["start"][max(0, j - period + 1) : j + 1]) < demand[j]:
            error_list.append(f"The demand for day {j+1} is not met")

    return error_list


if __name__ == "__main__":
    print(run())

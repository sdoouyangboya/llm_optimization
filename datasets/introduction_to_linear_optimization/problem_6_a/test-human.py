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

    if not "v" in all_json_keys:
        error_list.append("The output field 'v' is missing")

    if not "a" in all_json_keys:
        error_list.append("The output field 'a' is missing")

    if not "fuel_spend" in all_json_keys:
        error_list.append("The output field 'fuel_spend' is missing")

    if abs(output["x"][0] - data["x_0"]) > eps:
        error_list.append("The initial position is not correct")

    if abs(output["v"][0] - data["v_0"]) > eps:
        error_list.append("The initial velocity is not correct")

    if abs(output["x"][-1] - data["x_T"]) > eps:
        error_list.append("The final position is not correct")

    if abs(output["v"][-1] - data["v_T"]) > eps:
        error_list.append("The final velocity is not correct")

    for t in range(1, data["T"]):
        if abs(output["x"][t] - output["x"][t - 1] - output["v"][t - 1]) > eps:
            error_list.append(f"The position at time {t} is not consistent")

        if abs(output["v"][t] - output["v"][t - 1] - output["a"][t - 1]) > eps:
            error_list.append(f"The velocity at time {t} is not consistent")

    if abs(sum([abs(a) for a in output["a"]]) - output["fuel_spend"]) > eps:
        error_list.append("The total fuel spent is not correct")

    return error_list


if __name__ == "__main__":
    print(run())

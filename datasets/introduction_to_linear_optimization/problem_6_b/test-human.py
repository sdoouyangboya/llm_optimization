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

    for key in ["x", "v", "a"]:
        if not isinstance(output[key], list):
            error_list.append(f"The output field '{key}' is not a list")
    if not isinstance(output["fuel_spend"], (int, float)):
        error_list.append(
            f"The output field 'fuel_spend' is {output['fuel_spend']} which is not a number."
        )

    if len(error_list) > 0:
        return error_list

    # if (
    #     len(output["x"]) != data["T"]
    #     or len(output["v"]) != data["T"]
    #     or len(output["a"]) != data["T"]
    # ):
    #     error_list.append(
    #         f"The length of the output lists x, v, and a is {len(output['x'])}, {len(output['v'])}, {len(output['a'])} instead of {data['T']}"
    #     )

    if (
        abs(output["x"][0] - data["x_0"]) > eps
        or abs(output["v"][0] - data["v_0"]) > eps
    ):
        error_list.append(
            "The initial position or velocity does not match the input data"
        )

    if (
        abs(output["x"][-1] - data["x_T"]) > eps
        or abs(output["v"][-1] - data["v_T"]) > eps
    ):
        error_list.append(
            "The final position or velocity does not match the input data"
        )

    for t in range(data["T"] - 1):
        if abs(output["x"][t + 1] - output["x"][t] - output["v"][t]) > eps:
            error_list.append(
                f"The position at time {t+1} is not consistent with the velocity at time {t}"
            )
        if abs(output["v"][t + 1] - output["v"][t] - output["a"][t]) > eps:
            error_list.append(
                f"The velocity at time {t+1} is not consistent with the acceleration at time {t}"
            )

    if abs(sum(abs(a) for a in output["a"]) - output["fuel_spend"]) > eps:
        error_list.append(
            "The total fuel spent is not consistent with the sum of the absolute values of the accelerations"
        )

    return error_list


if __name__ == "__main__":
    print(run())

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

    if not "lower_bound" in all_json_keys:
        error_list.append("The output field 'lower_bound' is missing")

    if not "upper_bound" in all_json_keys:
        error_list.append("The output field 'upper_bound' is missing")

    if "lower_bound" in all_json_keys and not isinstance(
        output["lower_bound"], (int, float)
    ):
        error_list.append("The output field 'lower_bound' is not a number")

    if "upper_bound" in all_json_keys and not isinstance(
        output["upper_bound"], (int, float)
    ):
        error_list.append("The output field 'upper_bound' is not a number")

    if "lower_bound" in all_json_keys and "upper_bound" in all_json_keys:
        if output["lower_bound"] - output["upper_bound"] > eps:
            error_list.append("The 'lower_bound' is greater than 'upper_bound'")

    K = int(data["K"])
    if "lower_bound" in all_json_keys and (
        output["lower_bound"] < -eps or output["lower_bound"] - K**4 > eps
    ):
        error_list.append("The 'lower_bound' is not in the valid range [0, K^4]")

    if "upper_bound" in all_json_keys and (
        output["upper_bound"] < -eps or output["upper_bound"] - K**4 > eps
    ):
        error_list.append("The 'upper_bound' is not in the valid range [0, K^4]")

    return error_list


if __name__ == "__main__":
    print(run())

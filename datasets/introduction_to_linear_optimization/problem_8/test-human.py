import json
import numpy as np

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

    if not "power" in all_json_keys:
        error_list.append("The output field 'power' is missing")

    if not "error" in all_json_keys:
        error_list.append("The output field 'error' is missing")

    if "power" in all_json_keys:
        for i, power in enumerate(output["power"]):
            if power < -eps:
                error_list.append(f"The power of lamp {i+1} is negative: {power}")

    if "error" in all_json_keys:
        if output["error"] < -eps:
            error_list.append(f"The error is negative: {output['error']}")

    if "power" in all_json_keys and "coeff" in data and "desired" in data:
        coeff = np.array(data["coeff"])
        desired = np.array(data["desired"])
        power = np.array(output["power"])
        calculated_ill = np.dot(coeff, power)
        for i, (calc, des) in enumerate(zip(calculated_ill, desired)):
            if abs(calc - des) > output["error"] + eps:
                error_list.append(
                    f"The calculated illumination of segment {i+1} does not match the desired illumination within the acceptable error range. Calculated: {calc}, Desired: {des}"
                )

    return error_list


if __name__ == "__main__":
    print(run())

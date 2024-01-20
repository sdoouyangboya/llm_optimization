
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
    with open('data.json', 'r') as f:
        data = json.load(f)

    with open('output.json', 'r') as f:
        output = json.load(f)

    all_json_keys = []
    parse_json(output, all_json_keys)

    error_list = []

    if not "sellheifer" in all_json_keys:
        error_list.append("The output field 'sellheifer' is missing")

    if not "spacegrain" in all_json_keys:
        error_list.append("The output field 'spacegrain' is missing")

    if not "spacesugar" in all_json_keys:
        error_list.append("The output field 'spacesugar' is missing")

    # Check if the output values are valid
    for i in range(5):
        
        sellheifer = output["sellheifer"][i]
        spacegrain = output["spacegrain"][i]
        spacesugar = output["spacesugar"][i]

        # Check if the number of heifers to sell is valid
        if sellheifer < 0:
            error_list.append(f"The value of sellheifer in year {i+1} is invalid")

        # Check if the space for grain is valid
        if spacegrain < 0 or spacegrain > data["space_grain"]:
            error_list.append(f"The value of spacegrain in year {i+1} is invalid")

        # Check if the space for sugar beet is valid
        if spacesugar < 0 or spacesugar > data["all_space"] - data["space_grain"]:
            error_list.append(f"The value of spacesugar in year {i+1} is invalid")

    # This problem has not been solved

    return error_list


if __name__ == '__main__':
    print(run())

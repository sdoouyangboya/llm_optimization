
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

    if not "sell" in all_json_keys:
        error_list.append("The output field 'sell' is missing")

    if not "manufacture" in all_json_keys:
        error_list.append("The output field 'manufacture' is missing")

    if not "storage" in all_json_keys:
        error_list.append("The output field 'storage' is missing")

    # Check if the sell satisfies the marketing limitations
    for k in range(len(data["profit"])):
        for i in range(len(data["limit"][0])):
            if output["sell"][i][k] > data["limit"][k][i] + eps:
                error_list.append(f"The sell of product {k+1} in month {i+1} exceeds the marketing limitation")

    # Check the working time
    total_revenue = 0.0
    total_profit = 0.0
    total_cost = 0.0


    return error_list


if __name__ == '__main__':
    print(run())


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

    if not "isoperated" in all_json_keys:
        error_list.append("The output field 'isoperated' is missing")

    if not "amount" in all_json_keys:
        error_list.append("The output field 'amount' is missing")

    # Check if the number of operated mines in each year does not exceed the maximum limit
    n_mines = data["n_mines"]
    n_maxwork = data["n_maxwork"]
    isoperated = output["isoperated"]
    for i in range(len(isoperated[0])):
        if sum(isoperated[k][i] for k in range(n_mines)) > n_maxwork:
            error_list.append(f"The number of operated mines in year {i+1} exceeds the maximum limit")

    # Check if the amount of ore produced by each mine in each year does not exceed the upper limit
    limit = data["limit"]
    amount = output["amount"]
    for k in range(n_mines):
        for i in range(len(amount[k])):
            if amount[k][i] > limit[k]:
                error_list.append(f"The amount of ore produced by mine {k+1} in year {i+1} exceeds the upper limit")

    # Check if the blended ore quality in each year matches the required quality
    quality = data["quality"]
    requiredquality = data["requiredquality"]
    isoperated = output["isoperated"]
    amount = output["amount"]
    for i in range(len(isoperated[0])):
        total_quality = sum(amount[k][i] * quality[k] for k in range(n_mines) if isoperated[k][i])
        if abs(total_quality - requiredquality[i]) > eps:
            error_list.append(f"The blended ore quality in year {i+1} does not match the required quality")

    return error_list


if __name__ == '__main__':
    print(run())

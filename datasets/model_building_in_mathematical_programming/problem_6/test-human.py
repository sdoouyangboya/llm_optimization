
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

    if not "recruit" in all_json_keys:
        error_list.append("The output field 'recruit' is missing")

    if not "overmanning" in all_json_keys:
        error_list.append("The output field 'overmanning' is missing")

    if not "short" in all_json_keys:
        error_list.append("The output field 'short' is missing")

    recruit = output["recruit"]
    overmanning = output["overmanning"]
    short = output["short"]

    requirement = data["requirement"]
    strength = data["strength"]
    lessonewaste = data["lessonewaste"]
    moreonewaste = data["moreonewaste"]
    recruit_limit = data["recruit"]
    cost_redundancy = data["costredundancy"]
    num_overman = data["num_overman"]
    cost_overman = data["costoverman"]
    num_shortwork = data["num_shortwork"]
    cost_short = data["costshort"]

    K = len(requirement)
    I = len(requirement[0])

    # Check if the recruit values are within the allowed limits
    for k in range(K):
        for i in range(I):
            if recruit[k][i] < 0 or recruit[k][i] > recruit_limit[k]:
                error_list.append(f"The recruit value for manpower {k+1} in year {i+1} is out of range")

    # Check if the overmanning values are within the allowed limits
    for k in range(K):
        for i in range(I):
            if overmanning[k][i] < 0 or overmanning[k][i] > num_overman:
                error_list.append(f"The overmanning value for manpower {k+1} in year {i+1} is out of range")

    # Check if the short values are within the allowed limits
    for k in range(K):
        for i in range(I):
            if short[k][i] < 0 or short[k][i] > num_shortwork:
                error_list.append(f"The short value for manpower {k+1} in year {i+1} is out of range")

    # Check if the total manpower requirement is satisfied
    for k in range(K):
        for i in range(I):
            total_manpower = strength[k] + recruit[k][i] - lessonewaste[k] - moreonewaste[k] + overmanning[k][i] - short[k][i]
            if total_manpower < requirement[k][i] - eps:
                error_list.append(f"The total manpower for manpower {k+1} in year {i+1} is less than the requirement")

    return error_list


if __name__ == '__main__':
    print(run())

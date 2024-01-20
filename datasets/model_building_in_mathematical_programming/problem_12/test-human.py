
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

    if not "islocated" in all_json_keys:
        error_list.append("The output field 'islocated' is missing")

    # Check if each department is located in a valid city
    islocated = output.get("islocated")
    if islocated:
        for k, locations in enumerate(islocated):
            count = 0
            for l, is_located in enumerate(locations):
                if is_located:
                    count += 1
                    if count > 3:
                        error_list.append(f"Department {k+1} is located in more than 3 cities")
                    if l >= len(data["benefit"][k]):
                        error_list.append(f"Department {k+1} is located in an invalid city")

    return error_list


if __name__ == '__main__':
    print(run())

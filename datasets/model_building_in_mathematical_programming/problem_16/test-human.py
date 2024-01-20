
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

    if not "numon" in all_json_keys:
        error_list.append("The output field 'numon' is missing")


    numon = output["numon"]
    num = data["num"]
    minlevel = data["minlevel"]
    maxlevel = data["maxlevel"]

    if len(numon) != len(num):
        error_list.append("The number of generator types in the output does not match the input")

    for k in range(len(num)):
        if len(numon[k]) != len(data["demand"]):
            error_list.append(f"The number of periods in the output for generator type {k+1} does not match the input")

        for t in range(len(data["demand"])):
            if numon[k][t] < 0 or numon[k][t] > num[k]:
                error_list.append(f"The number of generators of type {k+1} on in period {t+1} is invalid")

    for k in range(len(num)):
        for t in range(len(data["demand"])):
            if numon[k][t] > 0:
                if numon[k][t] > data["num"][k]:
                    error_list.append(f"The number of generators of type {k+1} on in period {t+1} is outside the valid range")

    return error_list


if __name__ == '__main__':
    print(run())


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

    if not "produce" in all_json_keys:
        error_list.append("The output field 'produce' is missing")

    if not "buildcapa" in all_json_keys:
        error_list.append("The output field 'buildcapa' is missing")

    if not "stockhold" in all_json_keys:
        error_list.append("The output field 'stockhold' is missing")

    # Check if the output is consistent and valid
    produce = output["produce"]
    buildcapa = output["buildcapa"]
    stockhold = output["stockhold"]

    # Check if the dimensions of the output are correct
    K = len(data["inputone"])
    T = len(produce[0])
    if len(produce) != K or len(buildcapa) != K or len(stockhold) != K:
        error_list.append("The dimensions of the output are incorrect")

    # Check if the output satisfies the constraints
    for t in range(T):
        for k in range(K):

            # Check if the manpower capacity is not exceeded
            manpower = data["manpowerone"][k] + data["manpowertwo"][k]
            if t > 0:
                manpower += buildcapa[k][t-1]
            if manpower > data["manpower_limit"]:
                error_list.append(f"The manpower capacity for industry {k+1} in year {t+1} is exceeded")

            # Check if the demand is satisfied
            if t > 0:
                demand = data["demand"][k]
                for j in range(K):
                    demand += data["inputone"][j][k] * produce[j][t-1]
                    demand += data["inputtwo"][j][k] * buildcapa[j][t-1]
                if produce[k][t] + stockhold[k][t-1] + buildcapa[k][t-1] < demand - eps:
                    error_list.append(f"The demand for industry {k+1} in year {t+1} is not satisfied")

    return error_list


if __name__ == '__main__':
    print(run())

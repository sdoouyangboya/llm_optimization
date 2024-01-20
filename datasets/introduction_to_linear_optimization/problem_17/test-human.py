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

    if not "sell" in all_json_keys:
        error_list.append("The output field 'sell' is missing")
    else:
        sell = output["sell"]
        if len(sell) != len(data["bought"]):
            error_list.append(
                f"The length of 'sell' list ({len(sell)}) is not equal to the length of 'bought' list ({len(data['bought'])})"
            )

        total_amount = 0
        for i in range(len(sell)):
            if sell[i] < -eps or sell[i] > data["bought"][i] + eps:
                error_list.append(
                    f"The number of shares to sell ({sell[i]}) for stock {i+1} is not in the valid range [0, {data['bought'][i]}]"
                )

            amount = (
                sell[i] * data["currentPrice"][i] * (1 - data["transactionRate"] / 100)
            )

            gain = sell[i] * (data["currentPrice"][i] - data["buyPrice"][i])
            if gain > eps:
                amount -= gain * data["taxRate"] / 100

            total_amount += amount

        if total_amount < data["K"] - eps:
            error_list.append(
                f"The total amount raised ({total_amount}) is less than the required amount ({data['K']})"
            )

    if not "expectedValue" in output:
        error_list.append("The output field 'expectedValue' is missing")
    else:
        expectedValue = 0  # expected value of the portfolio next year
        for i in range(len(sell)):
            expectedValue += (data["bought"][i] - sell[i]) * data["futurePrice"][i]

        if abs(expectedValue - output["expectedValue"]) > eps:
            error_list.append(
                f"The expected value of the portfolio next year ({expectedValue}) is not equal to the expected value in the json output ({output['expectedValue']})"
            )

    return error_list


if __name__ == "__main__":
    print(run())

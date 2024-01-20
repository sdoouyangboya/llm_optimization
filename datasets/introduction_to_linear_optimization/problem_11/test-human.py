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

    if not "transactions" in all_json_keys:
        error_list.append("The output field 'transactions' is missing")

    if not "from" in all_json_keys:
        error_list.append("The output field 'from' is missing")

    if not "to" in all_json_keys:
        error_list.append("The output field 'to' is missing")

    if not "amount" in all_json_keys:
        error_list.append("The output field 'amount' is missing")

    if not "final_amount_of_currency_N" in all_json_keys:
        error_list.append("The output field 'final_amount_of_currency_N' is missing")

    limit_left = data["limit"]
    # Check if the total amount of each currency exchanged does not exceed the limit
    total_amount_exchanged = [0] * len(data["start"])
    for transaction in output["transactions"]:
        total_amount_exchanged[int(transaction["from"]) - 1] -= transaction["amount"]
        total_amount_exchanged[int(transaction["to"]) - 1] += (
            transaction["amount"]
            * data["rate"][int(transaction["from"]) - 1][int(transaction["to"]) - 1]
        )

        limit_left[int(transaction["from"]) - 1] -= transaction["amount"]
        limit_left[int(transaction["to"]) - 1] -= (
            transaction["amount"]
            * data["rate"][int(transaction["from"]) - 1][int(transaction["to"]) - 1]
        )

    for i, amount in enumerate(limit_left):
        if amount < -eps:
            error_list.append(
                f"The total amount of currency {i+1} exchanged ({total_amount_exchanged[i]}) is more than the limit ({data['limit'][i]})"
            )

    # Check to make sure at least one limit is depleted
    if all([x > eps for x in limit_left]):
        error_list.append(f"At least one limit should be depleted. Got: {limit_left}")

    # Check if the total amount of each currency exchanged is not more than the starting amount
    for i, amount in enumerate(total_amount_exchanged):
        if abs(amount + data["start"][i]) > eps:
            error_list.append(
                f"The total amount of currency {i+1} exchanged ({amount}) is more than the starting amount ({data['start'][i]})"
            )

    # Check if the final amount of currency N is correctly calculated
    final_amount = data["start"][-1] + total_amount_exchanged[-1]
    if abs(final_amount - output["final_amount_of_currency_N"]) > eps:
        error_list.append(
            f"The final amount of currency N is incorrectly calculated. Expected: {final_amount}, Got: {output['final_amount_of_currency_N']}"
        )

    return error_list


if __name__ == "__main__":
    print(run())

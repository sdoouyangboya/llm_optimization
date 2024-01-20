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

    # Check if all required keys are present
    required_keys = [
        "system_output",
        "num_produced",
        "total_256K_boards_used",
        "total_alt_boards_used",
        "total_disk_drives_used",
        "profit",
    ]

    for key in required_keys:
        if key not in all_json_keys:
            error_list.append(f"The output field '{key}' is missing")

    # Check if any of the values in the output are not numbers or are negative

    for i, system in enumerate(output["system_output"]):
        for key in [
            "num_produced",
            "total_256K_boards_used",
            "total_alt_boards_used",
            "total_disk_drives_used",
        ]:
            if not isinstance(system[key], (int, float)):
                error_list.append(
                    f"The value of '{key}' for system {i+1} is not a number"
                )
            elif system[key] < -eps:
                error_list.append(f"The value of '{key}' for system {i+1} is negative")

    if not isinstance(output["profit"], (int, float)):
        error_list.append("The value of 'profit' is not a number")
    elif output["profit"] < -eps:
        error_list.append("The value of 'profit' is negative")

    if len(error_list) > 0:
        return error_list

    # Check if the total number of produced systems does not exceed the maximum demand for each system
    for i, system in enumerate(output["system_output"]):
        if system["num_produced"] - data["demand"][i] > eps:
            error_list.append(f"Produced more than the maximum demand for system {i+1}")

    # Check if the total number of produced GP and WS systems does not exceed the maximum demand for the GP and WS families
    total_GP = sum(
        system["num_produced"]
        for i, system in enumerate(output["system_output"])
        if not data["is_workstation"][i]
    )
    total_WS = sum(
        system["num_produced"]
        for i, system in enumerate(output["system_output"])
        if data["is_workstation"][i]
    )
    if total_GP - data["demand_GP"] > eps:
        error_list.append("Produced more than the maximum demand for the GP family")
    if total_WS - data["demand_WS"] > eps:
        error_list.append("Produced more than the maximum demand for the WS family")

    # Check if the total number of disk drives used does not exceed the available disk drives
    total_disk = sum(
        system["total_disk_drives_used"] for system in output["system_output"]
    )
    if total_disk - data["max_disk"] > eps or total_disk - data["min_disk"] < -eps:
        error_list.append(
            f"Disk drive usage ({total_disk}) is out of demand range {data['min_disk']} - {data['max_disk']}"
        )

    # Check if the total number of 256K memory boards used does not exceed the available 256K memory boards
    total_256K = sum(
        system["total_256K_boards_used"] for system in output["system_output"]
    )
    if total_256K - data["max_mem"] > eps or total_256K - data["min_mem"] < -eps:
        error_list.append(
            f"256K memory board usage ({total_256K}) is out of demand range {data['min_mem']} - {data['max_mem']}"
        )

    # Check if the total number of alternative memory boards used does not exceed the available alternative memory boards
    total_alt = sum(
        system["total_alt_boards_used"] for system in output["system_output"]
    )
    if total_alt - data["alt_mem"] > eps:
        error_list.append(
            f"Alternative memory board usage ({total_alt}) is out of demand range 0 - {data['alt_mem']}"
        )

    # Check if the number of preordered systems is fulfilled
    for i, system in enumerate(output["system_output"]):
        if data["preorder"][i] - system["num_produced"] > eps:
            error_list.append(f"Did not fulfill the preorder for system {i+1}")

    # Check if the alternative memory boards are only used in compatible systems
    for i, system in enumerate(output["system_output"]):
        if system["total_alt_boards_used"] > eps and not data["alt_compatible"][i]:
            error_list.append(
                f"Used alternative memory boards in incompatible system {i+1}"
            )

    return error_list


if __name__ == "__main__":
    print(run())

import json

eps = 1e-03


def run():

    error_list = []

    with open('data.json', 'r') as f:
        data = json.load(f)

    try:
        with open('output.json', 'r') as f:
            output = json.load(f)
    except FileNotFoundError:
        error_list.append("Some constraints are missing and the problem is unbounded! Please double check")

    if "whichdisk" not in output:
        error_list.append("Missing whichdisk in output!")
    if "n_disks" not in output:
        error_list.append("Missing N in output!")

    all_disks = []
    for item in output["whichdisk"]:
        if item not in all_disks:
            all_disks.append(item)

    if len(all_disks) != output["n_disks"]:
        error_list.append("The solution shows %d disks are needed. But only %d are actually used " % \
               (output["n_disks"], len(all_disks)))

    return error_list

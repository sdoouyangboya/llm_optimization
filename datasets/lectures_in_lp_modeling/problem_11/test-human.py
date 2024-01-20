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

    if "number" not in output:
        error_list.append("Missing number in output!")

    n_ports = len(data["numdepot"])

    for i in range(n_ports):
        for j in range(n_ports):
            if output["number"][i][j] < 0:
                error_list.append("The quantity sent from port %d to depot %d is negative." % (i + 1, j + 1))

    source = data["numdepot"]
    sink = data["numport"]

    # Check in = out
    for i in range(n_ports):
        for j in range(n_ports):
            move_num = output["number"][i][j]
            source[i] -= move_num
            sink[j] -= move_num
            if source[i] < 0:
                error_list.append("There are more containers sent from depot %d than it has" % (i + 1))
            if sink[i] < 0:
                error_list.append("There are more containers arriving at port %d than it needs" % (i + 1))

    return error_list

if __name__ == '__main__':
    print(run())
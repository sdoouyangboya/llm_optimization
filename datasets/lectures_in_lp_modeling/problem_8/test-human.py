import json

eps = 1e-03

def check_validate(is_work, n_work, n_rest):

    n_days = len(is_work)
    started_working = 0
    idx = 0

    while idx < n_days:
        # If one is working
        if is_work[idx] == 1:
            started_working = 1
            if sum(is_work[idx:idx + n_work]) != n_work:
                return "not working for %d days in a row" % n_work
            idx += n_work
            if idx < n_days:
                if is_work[idx] != 0:
                    return "not working after resting"
            continue

        if is_work[idx] == 0 and started_working:
            if sum(is_work[idx:idx + n_rest]) != 0:
                return "not resting for %d days in a row" % n_rest
            idx += n_rest
            if idx < n_days:
                if is_work[idx] != 1:
                    return "not resting after working"
            continue

        if not started_working:
            idx += 1

    return "OK"

def run():

    error_list = []

    with open('data.json', 'r') as f:
        data = json.load(f)

    try:
        with open('output.json', 'r') as f:
            output = json.load(f)
    except FileNotFoundError:
        error_list.append("Some constraints are missing and the problem is unbounded! Please double check")

    if "is_work" not in output:
        error_list.append("Missing is_work in output!")

    if "total_number" not in output:
        error_list.append("Missing total_number in output!")

    # Verify whether each employee is working overtime
    n_employees = output["total_number"]
    
    # Record how long each employee has worked
    continuous_working_time = [0] * n_employees
    # Record how long each employee has rested
    continuous_resting_time = [0] * n_employees

    if len(output["is_work"]) != n_employees:
        error_list.append("Number of working employees cannot match the is_work table")
        return error_list

    for i in range(n_employees):
        info = check_validate(output["is_work"][i], data["n_working_days"], data["n_resting_days"])
        if info != "OK":
            error_list.append("Employee %d is %s" % (i + 1, info))

    # Check if there are sufficient people
    for n in range(len(data["num"])):
        n_working_employees = sum([output["is_work"][i][n] for i in range(n_employees)])
        if n_working_employees < data["num"][n]:
            error_list.append("Number of working employees is insuffient on day %d ", (n + 1))


    return error_list

if __name__ == '__main__':
    print(run())

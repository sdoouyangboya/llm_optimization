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

    if not "assignment" in all_json_keys:
        error_list.append("The output field 'assignment' is missing")

    if not "total_distance" in all_json_keys:
        error_list.append("The output field 'total_distance' is missing")

    # Check if the total number of students assigned from each neighborhood for each grade is equal to the population of that grade in that neighborhood
    for n, neighborhood in enumerate(data["population"]):
        for g, grade in enumerate(neighborhood):
            if (
                abs(
                    sum(
                        output["assignment"][n][s][g]
                        for s in range(len(data["capacity"]))
                    )
                    - grade
                )
                > eps
            ):
                error_list.append(
                    f"The total number of students assigned from neighborhood {n+1} for grade {g+1} is not equal to the population of that grade in that neighborhood"
                )

    # Check if the total number of students assigned to each school for each grade does not exceed the capacity of that grade in that school
    for s, school in enumerate(data["capacity"]):
        for g, grade in enumerate(school):
            if (
                sum(
                    output["assignment"][n][s][g]
                    for n in range(len(data["population"]))
                )
                - grade
                > eps
            ):
                error_list.append(
                    f"The total number of students assigned to school {s+1} for grade {g+1} exceeds the capacity of that grade in that school"
                )

    # Check if the total distance is equal to the sum of the product of the number of students assigned and the distance for each neighborhood, school, and grade
    total_distance = sum(
        sum(
            sum(
                output["assignment"][n][s][g] * data["distance"][n][s]
                for g in range(len(data["population"][n]))
            )
            for s in range(len(data["capacity"]))
        )
        for n in range(len(data["population"]))
    )

    for n in range(len(data["population"])):
        for s in range(len(data["capacity"])):
            for g in range(len(data["population"][n])):
                print(
                    f' {output["assignment"][n][s][g]} students from neighborhood {n+1} assigned to school {s+1} for grade {g+1}'
                )
                print(
                    f'the distance from neighborhood {n+1} to school {s+1} is {data["distance"][n][s]}'
                )
                print(
                    f'total distance for them is {output["assignment"][n][s][g] * data["distance"][n][s]}'
                )
    print(
        [
            [
                (output["assignment"][n][s][g], data["distance"][n][s])
                for g in range(len(data["population"][n]))
            ]
            for s in range(len(data["capacity"]))
        ]
    )
    if abs(total_distance - output["total_distance"]) > eps:
        error_list.append(
            f"The total distance in the output ({output['total_distance']}) is not equal to the calculated total distance ({total_distance})"
        )

    return error_list


if __name__ == "__main__":
    print(run())

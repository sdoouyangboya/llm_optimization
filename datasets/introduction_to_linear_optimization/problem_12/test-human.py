import json
import numpy as np

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

    if not "center" in all_json_keys:
        error_list.append("The output field 'center' is missing")

    if not "radius" in all_json_keys:
        error_list.append("The output field 'radius' is missing")

    if "center" in all_json_keys and "radius" in all_json_keys:
        center = np.array(output["center"])
        radius = output["radius"]

        if radius < -eps:
            error_list.append(f"The radius is negative: {radius}")

        A = np.array(data["A"])
        b = np.array(data["b"])

        for i in range(len(A)):
            if np.dot(A[i], center) - b[i] > eps:
                error_list.append(
                    f"The center of the ball is not within the set P for constraint {i+1}"
                )

        for i in range(len(center)):
            point_plus = center.copy()
            point_plus[i] += radius
            point_minus = center.copy()
            point_minus[i] -= radius

            for j in range(len(A)):
                if (
                    np.dot(A[j], point_plus) - b[j] > eps
                    or np.dot(A[j], point_minus) - b[j] > eps
                ):
                    error_list.append(
                        f"A point on the boundary of the ball is not within the set P for constraint {j+1}"
                    )

    return error_list


if __name__ == "__main__":
    print(run())

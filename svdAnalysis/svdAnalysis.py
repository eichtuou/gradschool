"""This script performs SVD analysis on a CSV data file of the following format:
    ,x1,y1,y2,y3,y4,...,yn,
    x2,y1,y2,y3,y4,...,yn,
    ...
    xn,y1,y2,y3,y4,...,yn,

(1) Lines starting with # are considered comments and are ignored.
(2) First column corresponds to the "x-axis" and is ignored when building the
    data matrix.
"""

import argparse
import numpy as np


def parse_arguments():
    """Validate input arguments

    Returns
    ----------
    args : argparse obj
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Perform SVD on a CSV data file.")
    parser.add_argument(
        "csv", type=str, help="Path to the input CSV file."
    )

    args = parser.parse_args()

    if not args.csv.endswith(".csv"):
        raise ValueError("Error! Input file must be in CSV format.")

    return args


def get_data(csv_file):
    """Read and process the data from the CSV file.

    Parameters
    ----------
    csv_file : str
        The name of the input CSV file.

    Returns
    -------
    data : np.array
        Array with y-values from the CSV file.
    """
    data = []

    with open(csv_file, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("#") or not line:
                continue

            # trim first and last commas if present
            line = line.strip(",").split(",")
            line = line[1:]

            data.append([float(value) for value in line])

    data = np.array(data)

    return data


def perform_svd(csv_file, data):
    """Perform Singular Value Decomposition (SVD) on the data matrix
    and save the VT matrix components to a file.

    Parameters
    ----------
    csv_name : str
        The name of the input CSV file.
    data : np.array
        Array with y-values from the CSV file.

    Returns
    -------
    None
    """
    _, _, vt = np.linalg.svd(data)
    output_file = f"{csv_file[:-4]}-vt-matrix.csv"

    with open(output_file, 'w') as file:
        for i, row in enumerate(vt):
            bufer = ", ".join(f"{value:.6f}" for value in row)
            file.write(f"VT component #{i + 1}, {bufer}\n")

    return None


def main():
    """Main program."""
    args = parse_arguments()
    input_file = args.csv
    data = get_data(input_file)
    perform_svd(input_file, data)

    return None


if __name__ == "__main__":
    main()

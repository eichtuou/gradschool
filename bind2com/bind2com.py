"""This script converts a BIND file into a COM file."""

import argparse
from itertools import islice


def parse_arguments():
    """Validate input arguments

    Returns
    ----------
    args : argparse obj
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert a BIND file to a COM file."
    )
    parser.add_argument(
        "bindfile",
        type=str,
        help="Path to the BIND file."
    )

    args = parser.parse_args()

    if not args.bindfile.endswith(".bind"):
        raise argparse.ArgumentTypeError("Error! File is not a BIND file.")

    return args


def flag_lines(bindfile):
    """Find line numbers containing information of interest.

    Parameters
    ----------
    bindfile : str
        Path to the BIND file

    Returns
    ----------
    flags : lst (int)
        List with flagged line numbers.
    """

    flags = []
    with open(bindfile, 'r') as file:
        jump_line = False
        for num, line in enumerate(file, 2):
            if "Geometry Crystallographic" in line:
                flags.append(num)
            elif "&" in line:
                if jump_line is False:
                    flags.append(num - 1)
                    jump_line = True
            elif "Crystal Spec" in line:
                flags.append(num)
                break

    return flags


def get_lattice(bindfile, flags):
    """Get lattice parameters

    Parameters
    ----------
    bindfile : str
        Path to the BIND file
    flags : lst (int)
        List with flagged line numbers.

    Returns
    ----------
    lattice : tuple (str)
        Lattice parameters (a, b, c)
    """
    with open(bindfile) as lines:
        line = next(islice(lines, flags[-1], flags[-1] + 1), None)
        if line:
            lattice = tuple(map(lambda x: format(
                float(x), '.9f'), line.strip().split()[:3])
            )
            return lattice

    return ("0.0", "0.0", "0.0")


def get_coords(bindfile, flags, lattice):
    """Get atomic coordinates and scale them with lattice parameters.

    Parameters
    ----------
    bindfile : str
        Path to the BIND file
    flags : lst (int)
        List with flagged line numbers.
    lattice : tuple (str)
        Lattice parameters (a, b, c)

    Returns
    ----------
    coords : lst (str)
        List of atomic coordinates, scaled with lattice information.
    """
    coords = []
    scaling_factors = list(map(float, lattice))

    with open(bindfile) as lines:
        for line in islice(lines, flags[0] + 1, flags[1] - 1):
            line = line.strip().split()
            xyz = [format(float(line[i]) * scaling_factors[i - 2], '.9f')
                   for i in range(2, 5)]
            coords.append(
                f"{line[0]} {line[1]} {xyz[0]} {xyz[1]} {xyz[2]}")

    return coords


def write_comfile(bindfile, coords, lattice):
    """Write the COM file.

    Parameters
    ----------
    bindfile : str
        Path to the BIND file
    coords : lst (str)
        List of atomic coordinates, scaled with lattice information.
    lattice : tuple (str)
        Lattice parameters (a, b, c)

    Returns
    ----------
    None
    """
    header = f"# hf/sto-3g\n\n{bindfile[:-5]}\n\n0 1\n"
    zeros = "0.000000000"
    lattice_vectors = [
        f"Tv {lattice[0]} {zeros} {zeros}",
        f"Tv {zeros} {lattice[1]} {zeros}",
        f"Tv {zeros} {zeros} {lattice[2]}"
    ]

    with open(bindfile[:-5] + ".com", 'w') as comfile:
        comfile.write(header)
        comfile.write("\n".join(coords) + "\n")
        comfile.write("\n".join(lattice_vectors) + "\n")

    return None


def main():
    """Main Program"""
    args = parse_arguments()
    bindfile = args.bindfile
    flags = flag_lines(bindfile)
    lattice = get_lattice(bindfile, flags)
    coords = get_coords(bindfile, flags, lattice)
    write_comfile(bindfile, coords, lattice)

    return None


if __name__ == "__main__":
    main()

"""This script translates an FCHK file to an XYZ file. Both filetypes
contain molecular structure information. FCHK is specific from
Gaussian09 while XYZ is widely used and can be read by various
molecular modeling softwares.
"""

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
        description="Convert a FCHK file to a XYZ file."
    )
    parser.add_argument(
        "fchkfile",
        type=str,
        help="Path to the FCHK file."
    )

    args = parser.parse_args()

    if not args.fchkfile.endswith(".fchk"):
        raise argparse.ArgumentTypeError("Error! File is not a FCHK file.")

    return args


def flag_lines(fchkfile):
    """Find line numbers containing information of interest.

    Parameters
    ----------
    fchkfile : str
        Path to the fchk file

    Returns
    ----------
    flags : dict
        Dictionary with flagged line numbers.
    """
    flags = {}

    with open(fchkfile, 'r') as file:
        for linenum, line in enumerate(file, 1):
            if 'Number of basis functions' in line:
                flags['nbasis'] = linenum
            elif 'Nuclear charges' in line:
                flags['nuclear_charges'] = linenum
            elif 'Current cartesian coordinates' in line:
                flags['cartesian_coords'] = linenum
            elif 'Force Field' in line:  # for stop
                flags['force_field'] = linenum
                break

    return flags


def get_charges_coords(fchkfile, flags):
    """Extract nuclear charges and cartesian coordinates from the FCHK file.

    Parameters
    ----------
    fchkfile : str
        Path to the FCHK file.
    flags : dict
        Dictionary with flagged line numbers.

    Returns
    -------
    tuple (lst)
        Tuple with two lists: element symbols, cartesian coordinates [Angs.]
    """

    element_map = {
        '1': 'H',
        '6': 'C', '7': 'N', '8': 'O', '9': 'F',
        '15': 'P', '16': 'S', '17': 'Cl',
        '22': 'Ti', '26': 'Fe', '27': 'Co', '28': 'Ni', '29': 'Cu',
        '30': 'Zn', '35': 'Br', '44': 'Ru', '53': 'I'
    }
    bohr_to_angs = 0.529177249
    nuclear_charges = []
    coordinates = []

    with open(fchkfile) as file:
        # get nuclear charges
        for line in islice(file, flags['nuclear_charges'], flags['cartesian_coords'] - 1):
            nuclear_charges.extend(
                map(lambda x: str(int(float(x))), line.split()))

        # map nuclear charge to element symbols
        nuclear_charges = [
            element_map.get(charge, charge)
            for charge in nuclear_charges
        ]

    with open(fchkfile) as file:
        # get cartesian coordinates
        for line in islice(file, flags['cartesian_coords'], flags['force_field'] - 1):
            coordinates.extend(map(float, line.split()))

    coordinates = [f"{coord * bohr_to_angs:.10f}" for coord in coordinates]

    if len(coordinates) != len(nuclear_charges) * 3:
        raise ValueError(
            "Error! Number of coordinates doesn't match number of atoms.")

    return nuclear_charges, coordinates


def write_xyz(fchkfile, flags):
    """Write the XYZ file.

    Parameters
    ----------
    fchkfile : str
        Path to the FCHK file.
    flags : dict
        Dictionary with flagged line numbers.

    Returns
    ----------
    None
    """
    nuclear_charges, coordinates = get_charges_coords(fchkfile, flags)
    xyz_file = fchkfile.replace(".fchk", ".xyz")

    with open(xyz_file, 'w') as file:
        file.write(f"{len(nuclear_charges)}\n{fchkfile}\n")

        for i, element in enumerate(nuclear_charges):
            x, y, z = coordinates[3 * i: 3 * i + 3]
            x = f"{float(x):12.10f}"
            y = f"{float(y):12.10f}"
            z = f"{float(z):12.10f}"
            file.write(f"{element:2}\t{x}\t{y}\t{z}\n")

    return None


def main():
    """Main Program"""
    args = parse_arguments()
    flags = flag_lines(args.fchkfile)
    write_xyz(args.fchkfile, flags)


if __name__ == "__main__":
    main()

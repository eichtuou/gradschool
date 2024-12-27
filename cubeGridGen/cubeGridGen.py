"""This script reads an molecular structure [XYZ] file and creates a
box around the system with a user specified "padding" in units of
Angstroms. The box is then partitioned into smaller boxes [inp_cube_*.dat],
which are then utilized as part of the input needed for performing parallel
denstity calculations of the whole system in Gaussian09.
"""

import argparse
import numpy as np
from itertools import product


def parse_arguments():
    """Validate input arguments

    Returns
    ----------
    args : argparse obj
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate grid inputs for Gaussian09 calculations.")
    parser.add_argument("xyzfile", type=str, help="Path to the XYZ file.")
    parser.add_argument(
        "--xpad",
        type=float,
        default=2.0,
        help="Padding in the x direction [Angs.].")
    parser.add_argument(
        "--ypad",
        type=float,
        default=2.0,
        help="Padding in the y direction [Angs.].")
    parser.add_argument(
        "--zpad",
        type=float,
        default=2.0,
        help="Padding in the z direction [Angs.].")
    parser.add_argument(
        "--nx",
        type=int,
        default=4,
        help="Number of partitions in the x direction (must be n+1 for n cubes).")
    parser.add_argument(
        "--ny",
        type=int,
        default=4,
        help="Number of partitions in the y direction (must be n+1 for n cubes).")
    parser.add_argument(
        "--nz",
        type=int,
        default=4,
        help="Number of partitions in the z direction (must be n+1 for n cubes).")
    parser.add_argument(
        "--xpts",
        type=int,
        default=175,
        help="Number of points in the x direction (resolution).")
    parser.add_argument(
        "--ypts",
        type=int,
        default=175,
        help="Number of points in the y direction (resolution).")
    parser.add_argument(
        "--zpts",
        type=int,
        default=175,
        help="Number of points in the z direction (resolution).")

    args = parser.parse_args()

    if not args.xyzfile.endswith(".xyz"):
        parser.error("The input file must be in XYZ format.")

    if any(value < 1 for value in (
        args.nx,
        args.ny,
        args.nz,
        args.xpts,
        args.ypts,
        args.zpts)
    ):
        parser.error(
            "Grid size and resolution must be greater than or equal to 1.")

    return args


def get_xyz_coords(xyzfile):
    """Get atomic coordinated from the XYZ file.

    Parameters
    ----------
    xyzfile : str
        Path to the XYZ file.

    Returns
    ----------
    x_coords, y_coords, z_coords : tuple (list)
        Lists of x, y, and z coordinates.
    """
    x_coords, y_coords, z_coords = [], [], []

    with open(xyzfile) as file:
        lines = file.readlines()[2:]
        for line in lines:
            _, x, y, z = line.split()
            x_coords.append(float(x))
            y_coords.append(float(y))
            z_coords.append(float(z))

    return x_coords, y_coords, z_coords


def get_min_max_coords(x_coords, y_coords, z_coords, x_pad, y_pad, z_pad):
    """Calculate the bounding box around molecule with specified padding.

    Parameters
    ----------
    x_coords : list (float)
        List of x coordinates.
    y_coords : list (float)
        List of y coordinates.
    z_coords : list (float)
        List of z coordinates.
    x_pad : float
        Padding in the x direction [Ang].
    y_pad : float
        Padding in the y direction [Ang].
    z_pad : float
        Padding in the z direction [Ang].

    Returns
    ----------
    min_coords, max_coords : tuple (list)
        Lists of minimum and maximum coordintes.
    """
    min_coords = [
        min(x_coords) - x_pad,
        min(y_coords) - y_pad,
        min(z_coords) - z_pad
    ]
    max_coords = [
        max(x_coords) + x_pad,
        max(y_coords) + y_pad,
        max(z_coords) + z_pad
    ]

    return min_coords, max_coords


def generate_grid(min_coords, max_coords, nx, ny, nz):
    """Generate coordinate grid.

    Parameters
    ----------
    min_coords : tuple (list)
        Lists of minimum coordintes.
    max_coords : tuple (list)
        Lists of maximum coordintes.
    nx : int
        Number of partitions in the x direction (must be n+1 for n cubes).
    ny : int
        Number of partitions in the y direction (must be n+1 for n cubes).
    nz : int
        Number of partitions in the z direction (must be n+1 for n cubes).

    Returns
    ----------
    dx, dy, dz, grid : tuple
        Step sizes (dx, dy, dz) and grid coordinates.
    """
    # step size
    dx = (max_coords[0] - min_coords[0]) / (nx - 1)
    dy = (max_coords[1] - min_coords[1]) / (ny - 1)
    dz = (max_coords[2] - min_coords[2]) / (nz - 1)

    # grid
    x_grid = np.delete(np.linspace(min_coords[0], max_coords[0], nx), nx - 1)
    y_grid = np.delete(np.linspace(min_coords[1], max_coords[1], ny), ny - 1)
    z_grid = np.delete(np.linspace(min_coords[2], max_coords[2], nz), nz - 1)
    grid = list(product(x_grid, y_grid, z_grid))

    if len(grid) != ((nx - 1) * (ny - 1) * (nz - 1)):
        raise ValueError("Mismatch between cube count and grid coordinates.")

    return dx, dy, dz, grid


def generate_input_files(xpts, ypts, zpts, dx, dy, dz, grid):
    """Generate input files for each cube in the grid.

    Parameters
    ----------
    xpts : int
        Points in the x direction (resolution).
    ypts : int
        Points in the y direction (resolution).
    zpts : int
        Points in the z direction (resolution).
    dx : float
        Step size in the x direction.
    dy : float
        Step size in the y direction.
    dz : float
        Step size in the z direction.
    grid : list (float)
        List of grid coordinates (cube origins).

    Returns
    ----------
    None
    """
    resolution = [
        f"{xpts}, {(dx / xpts):.9f}, 0.000000000, 0.000000000",
        f"{ypts}, 0.000000000, {(dy / ypts):.9f}, 0.000000000",
        f"{zpts}, 0.000000000, 0.000000000, {(dz / zpts):.9f}"
    ]

    for num, (x, y, z) in enumerate(grid, 1):
        input_file = f"inp_cube_{num}.dat"
        with open(input_file, 'w') as file:
            header = f"-1, {x:.9f}, {y:.9f}, {z:.9f}\n"
            file.write(header)
            for line in resolution:
                file.write(f"{line}\n")

    return None


def main():
    """Main Program."""
    args = parse_arguments()

    x_coords, y_coords, z_coords = get_xyz_coords(args.xyzfile)
    min_coords, max_coords = get_min_max_coords(
        x_coords, y_coords, z_coords, args.xpad, args.ypad, args.zpad)
    dx, dy, dz, grid = generate_grid(
        min_coords, max_coords, args.nx, args.ny, args.nz)
    generate_input_files(
        args.xpts,
        args.ypts,
        args.zpts,
        dx,
        dy,
        dz,
        grid)


if __name__ == "__main__":
    main()

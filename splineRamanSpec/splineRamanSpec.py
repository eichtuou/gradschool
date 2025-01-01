"""This script performs a cubic interpolation of Raman spectra and
generates a new spectrum file with a new x-range and averaged
y-values. To use this script, have only normalized and baseline
corrected spectra of one sample to be averaged in a single directory.
"""

import os
import argparse
import numpy as np
from scipy.interpolate import interp1d


def parse_arguments():
    """Validate input arguments

    Returns
    ----------
    args : argparse obj
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Perform cubic interpolation and average Raman spectra."
    )
    parser.add_argument(
        "x_initial",
        type=float,
        help="Initial x-value for interpolation.")
    parser.add_argument(
        "x_final",
        type=float,
        help="Final x-value for interpolation.")

    return parser.parse_args()


def get_spectra():
    """Get spectrum files in current directory.

    Returns
    -------
    spectra : list (str)
        List of spectrum (.DAT) files.
    """

    spectra = [file for file in os.listdir(os.getcwd()) if file.endswith(".dat")]

    return spectra


def cubic_interpolation(spectra, x_initial, x_final):
    """Perform cubic interpolation on all spectrum files.

    Parameters
    ----------
    spectra : list (str)
        List of spectrum (.DAT) files.
    x_initial : float
        Initial x-value for interpolation.
    x_final : float
        Final x-value for interpolation.

    Returns
    -------
    None
    """
    interpolated_y = []
    x_new = None

    # interpolate and save all spectra
    for spectrum in spectra:
        with open(spectrum, 'r') as file:
            lines = [line.strip().split() for line in file.readlines()]
            if x_new is None:
                x = np.array([float(line[0]) for line in lines])
                x_new = np.linspace(x_initial, x_final, len(x))
            y = np.array([float(line[1]) for line in lines])

        y_new = interp1d(x, y, kind='cubic')(x_new)

        new_spectrum = spectrum[:-4] + "-interpolated.dat"
        write_spectrum(new_spectrum, x_new, y_new)

        interpolated_y.append(y_new)

    # calculate average spectrum
    interpolated_y = np.array(interpolated_y)
    average_y = np.mean(interpolated_y, axis=0)
    write_spectrum("average-spectrum.dat", x_new, average_y)

    return None


def write_spectrum(spectrum_name, x_values, y_values):
    """Write spectrum file.

    Parameters
    ----------
    spectrum_name : str
        Name of spectrum file.
    x_values : np.array
        Array of x values.
    y_values : np.array
        Array of y values.

    Returns
    -------
    None
    """
    with open(spectrum_name, 'w') as file:
        for x_value, y_value in zip(x_values, y_values):
            file.write(f"{x_value:.6f}    {y_value:.6f}\n")

    return None


def main():
    """
    Main function to execute the script logic.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    args = parse_arguments()
    spectra = get_spectra()
    cubic_interpolation(spectra, args.x_initial, args.x_final)


if __name__ == "__main__":
    main()

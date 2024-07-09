"""This script gets excitations of interest from a log file of a TD-DFT
calculation from Gaussian09.
"""

import argparse
import linecache


def parse_input_params():
    """Parse input parameters.

    Parameters
    ----------
    None

    Returns
    ----------
    args : obj
        Argparse object containing parsed input parameters.
    """
    parser = argparse.ArgumentParser(
        description="Analyze TD-DFT calculations from Gaussian09 log files.")
    parser.add_argument('logfile',
                        help="Path to Gaussian09 log file.")
    parser.add_argument('-nm_min', metavar='', type=float, default=50,
                        help="Minimum excitation wavelength in nm.")
    parser.add_argument('-nm_max', metavar='', type=float, default=150,
                        help="Maximum excitation wavelength in nm.")
    parser.add_argument('-osc_min', metavar='', type=float, default=0.01,
                        help="Minimum oscillator strength.")
    args = parser.parse_args()

    return args


def get_excited_states(line, line_number, wavenum_min, wavenum_max,
                       oscillator_min, excited_states):
    """Get excited states with specific oscillator strength.

    Parameters
    ----------
    line : str
        Line from file.
    line_number : int
        Line number/index in file.
    wavenum_min : float
        Minimum excitation wavelength in nm.
    wavenum_max : float
        Maximum excitation wavelength in nm.
    oscillator_min : float
        Minimum oscillator strength.
    excited_states : dict
        Dictionary containing excited states of interest and their respective
        line number.

    Returns
    ----------
    None
    """
    line = line.split()
    wavenum = float(line[6])
    oscillator = float(line[8].replace('f=', ''))

    if wavenum >= wavenum_min and wavenum <= wavenum_max \
            and oscillator >= oscillator_min:
        excited_states[int(line[2].replace(':', ''))] = line_number

    return None


def read_logfile(logfile, wavenum_min=50, wavenum_max=150, oscillator_min=0.01):
    """Read log file and identify lines with excitated states of interest.

    Parameters
    ----------
    logfile : str
        Name of logfile.
    wavenum_min : float
        Minimmum excitation wavelength in nm.
    wavenum_max : float
        Maximum excitation wavelength in nm.
    oscillator_min : float
        Minimum oscillator strength.

    Returns
    ----------
    excited_states : dict
        Dictionary containing excited states of interest and their respective
        line number.
    """
    excited_states = {}

    with open(logfile, 'r') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if 'Excited State' in line:
                get_excited_states(line, line_number, wavenum_min, wavenum_max,
                                   oscillator_min, excited_states)

    return excited_states


def get_orbitals(line, orbitals):
    """Get orbital contributions to excited state.

    Parameters
    ----------
    line : str
        Line from file.
    orbitals : dict
        Dictionary containing the excited state orbitals.

    Returns
    ----------
    None
    """
    line = line.split()
    orbitals["contributions"].extend([f"{(2 * float(line[3]) ** 2):.2f}"])
    orbitals["occupied"].extend([line[0]])
    orbitals["virtual"].extend([line[2]])
    orbitals["coefficients"].extend([line[3]])

    return None


def write_output(logfile, excited_states):
    """Write output file with excited states and orbital contributions.

    Parameters
    ----------
    logfile : str
        Name of logfile.
    excited_states : dict
        Dictionary containing excited states of interest and their respective
        line number.

    Returns
    ----------
    None
    """
    line_numbers = list(excited_states.values())

    with open(logfile[:-4] + '_excitations.dat', 'w') as outfile:
        for line_number in line_numbers:
            line = linecache.getline(logfile, line_number).strip()
            line = line.split()

            text_buffer = (f"Excited State {line[2]}\n"
                           f"    nm = {line[6]}    f = {line[8][2:]}\n")

            orbitals = {
                "contributions": [],
                "occupied": [],
                "virtual": [],
                "coefficients": []
            }

            key_index = line_numbers.index(line_number)
            if key_index < len(line_numbers) - 1:
                max_iter = line_numbers[key_index +
                                        1] - line_numbers[key_index]
            else:
                max_iter = 500

            for i in range(1, max_iter):
                next_line = linecache.getline(logfile, line_number + i).strip()
                if '->' in next_line:
                    get_orbitals(next_line, orbitals)
                if 'Excited State' in next_line:
                    break

            for i in range(0, len(orbitals["contributions"])):
                text_buffer += "    " \
                    f"{orbitals["occupied"][i]} -> {orbitals["virtual"][i]}    "\
                    f"{orbitals["coefficients"][i]}    "\
                    f"contr = {orbitals["contributions"][i]}\n"

            outfile.write(text_buffer + "\n")

    return None


def main():
    """Main program."""
    args = parse_input_params()

    try:
        excited_states = read_logfile(
            args.logfile, args.nm_min, args.nm_max, args.osc_min)
        write_output(args.logfile, excited_states)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()

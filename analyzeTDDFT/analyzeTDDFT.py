"""This script gets excitations of interest from a log file of a TD-DFT
calculation from Gaussian09.

Run as: python analyzeTDDFT.py file.log
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
    args
    """
    parser = argparse.ArgumentParser(
        description="Analyze TD-DFT calculations from Gaussian09 log files.")
    parser.add_argument('logfile',
                        help="Path to the Gaussian09 log file.")
    parser.add_argument('-nm_min', type=int, default=50,
                        help="Minimum excitation wavelength in nm.")
    parser.add_argument('-nm_max', type=int, default=150,
                        help="Maximum excitation wavelength in nm.")
    parser.add_argument('-osc_min', type=float, default=0.01,
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
    nm_min : float
        Minimum excitation wavelength in nm.
    nm_max : float
        Maximum excitation wavelength in nm.
    fosc_min : float
        Minimum oscillator strength.
    states : dict
        Dictionary containing excited states of interest.

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
    """Read log file and identify lines with excitation information.

    Parameters
    ----------
    logfile :
    wavenum_min :
    wavenum_max :
    oscilaltor_min :

    Returns
    ----------
    excited_states :
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
    """Get orbital contributions to excited state and update lists.

    Parameters
    ----------
    line :
    index :

    Returns
    ----------


    """
    line = line.split()
    orbitals["contributions"].extend([f"{(2 * float(line[3]) ** 2):.2f}"])
    orbitals["occupied"].extend([line[0]])
    orbitals["virtual"].extend([line[2]])
    orbitals["coefficients"].extend([line[3]])

    return None

def write_output(logfile, indeces):
    """Write output file with excited states and orbital contributions.

    Parameters
    ----------
    logfile :
    index :

    Returns
    ----------
    None
    """
    indeces = indeces.values()

    with open(logfile[:-4] + '_excitations.dat', 'w') as outfile:
        for index in indeces:
            line = linecache.getline(logfile, index).strip()
            line = line.split()

            outfile.write(f"Excited State {line[2]}\n"
                          f"    nm = {line[6]}    f = {line[8][2:]}\n")

            orbitals = {
                "contributions": [],
                "occupied": [],
                "virtual": [],
                "coefficients": []
            }

            for i in range(1, 100):
                next_line = linecache.getline(logfile, index + i).strip()
                if '->' in next_line:
                    get_orbitals(next_line, orbitals)
                if 'Excited State' in next_line:
                    break

            print(orbitals)
            for i in range(len(orbitals)):
                #outfile.write(f"    {orbs_occupied[i]} -> {virtual[i]}    {coefficients[i]}    "
                #              f"contr = {contributions[i]}\n"
                print(f"    {orbitals["occupied"]} -> {orbitals["virtual"]}    {orbitals["coefficients"]}    "
                              f"contr = {orbitals["contributions"]}\n")

            #outfile.write('\n')

    return None


def main():
    """Main program."""
    args = parse_input_params()

    try:
        states = read_logfile(args.logfile, args.nm_min, args.nm_max, args.osc_min)
        write_output(args.logfile, states)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()


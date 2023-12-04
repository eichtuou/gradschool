"""This script gets excitations of interest from a log file of a TD-DFT
calculation from Gaussian09.

Run as: python analyzeTDDFT.py file.log
"""

import sys
import argparse
import linecache


def get_states(line, line_number, nm_init, nm_final, f_osc_min, states, index):
    """Get excited states with specific oscillator strength."""
    line = line.split()
    nm = float(line[6])
    f_osc = float(line[8].replace('f=', ''))

    if nm >= nm_init and nm <= nm_final and f_osc >= f_osc_min:
        states.append(int(line[2].replace(':', '')))
        index.append(line_number)

    return None


def read_log_file(logfile, nm_min=50, nm_max=150, f_osc_min=0.01):
    """Read log file and identify lines with excitation information."""
    states = []
    index = []

    with open(logfile, 'r') as file:
        for i, line in enumerate(file, 1):
            line = line.strip()
            if 'Excited State' in line:
                get_states(line, i, nm_min, nm_max, f_osc_min, states, index)

    return states, index


def get_orbitals(line, occ, virt, coeff, contr):
    "Get orbital contributions to excited state."
    elements = line.split()
    contr_value = 2 * float(elements[3]) ** 2
    occ.append(int(elements[0]))
    virt.append(int(elements[2]))
    coeff.append(elements[3])
    contr.append(f"{contr_value:.2f}")

    return None


def write_output_file(logfile, index):
    """Write output file with excited states and orbital contributions."""
    with open(logfile[:-4] + '_excitations.dat', 'w') as outf:
        for i in index:
            line = linecache.getline(logfile, i).strip()
            line = line.split()

            outf.write(f"Excited State {line[2]}\n"
                       f"    nm = {line[6]}    f = {line[8][2:]}\n")

            occ, virt, coeff, contr = [], [], [], []

            for j in range(1, 100):
                next_line = linecache.getline(logfile, i + j).strip()
                if '->' in next_line:
                    get_orbitals(next_line, occ, virt, coeff, contr)
                if 'Excited State' in next_line:
                    break

            for k in range(len(occ)):
                outf.write(f"    {occ[k]} -> {virt[k]}    {coeff[k]}    "
                           f"contr = {contr[k]}\n")

            outf.write('\n')

    return None


def main():
    """Main program."""
    parser = argparse.ArgumentParser(
        description="Analyze TD-DFT calculations from Gaussian09 log files.")
    parser.add_argument('logfile',
                        help="Path to the Gaussian09 log file.")
    parser.add_argument('--nm_min', type=int, default=50,
                        help="Minimum excitation wavelength in nm.")
    parser.add_argument('--nm_max', type=int, default=150,
                        help="Maximum excitation wavelength in nm.")
    parser.add_argument('--f_osc_min', type=float, default=0.01,
                        help="Minimum oscillator strength.")
    args = parser.parse_args()

    try:
        states, index = read_log_file(args.logfile, args.nm_min, args.nm_max,
                                      args.f_osc_min)
        write_output_file(args.logfile, index)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()


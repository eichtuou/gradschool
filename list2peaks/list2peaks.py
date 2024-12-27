"""This script converts an NMR peak list file generated by NMRFAM-Sparky [LIST]
to a peak list file to be read by TopSpin [PEAKS].
"""

import argparse

def parse_arguments():
    """Validate input arguments

    Returns
    ----------
    args : argparse obj
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert NMR peak list file from LIST format to PEAKS format.")
    parser.add_argument("listfile", type=str, help="Path to the input LIST file.")
    parser.add_argument("--peaksfile", type=str, default="out.peaks", help="Path to the output PEAKS file.")

    args = parser.parse_args()

    if not args.listfile.endswith(".list"):
        parser.error("Input file must be in LIST format.")

    return args


def get_peak_info(listfile):
    """Get peak information from LIST file.

    Parameters
    ----------
    listfile : str
        Path to the input LIST file.

    Returns
    -------
    peaks : list (str)
        List of peaks.
    """
    peaks = []
    with open(listfile, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("Assignment"):
                continue
            peaks.append(line.split())

    return peaks


def write_peaksfile(peaksfile, peaks):
    """Write PEAKS file.

    Parameters
    ----------
    peaksfile : str
        Path to the output PEAKS file.
    peak : list (str)
        List of peaks.

    Returns
    -------
    None
    """
    with open(peaksfile, 'w') as file:
        file.write("# Number of dimensions 2\n")
        for num, peak in enumerate(peaks, start=1):
            peak_entry = (
                f"{num} {peak[1]} {peak[2]} 1 - 0.000E00 0.000E00 - 0 0 0 0\n"
                f"#{peak[0]}\n"
            )
            file.write(peak_entry)
    return None


def main():
    """Main Program."""
    args = parse_arguments()
    peaks = get_peak_info(args.listfile)
    write_peaksfile(args.peaksfile, peaks)


if __name__ == "__main__":
    main()

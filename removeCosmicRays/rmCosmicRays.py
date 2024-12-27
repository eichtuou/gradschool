"""This script processes Raman spectra files to:
    - Baseline correct and remove cosmic rays.
    - Apply toluene reference correction.
    - Generate an averaged corrected spectrum.

Spectra files should be in a single directory. Baseline correction points
and toluene reference peak positions are provided interactively, with the
option to load values from last session.
"""

import os
import json
import numpy as np

LOG_FILE = "last_values.json"


def load_log():
    """Load values from last session.

    Returns
    -------
    last_values : dict
        Last session values of baseline points and toluene peaks.
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            last_values = json.load(file)
    else:
        last_values = {"baseline_pts": [], "toluene_pks": []}

    return last_values


def save_log(baseline_pts, toluene_pks):
    """Save the current baseline points and toluene peaks to a log file.

    Parameters
    ----------
    baseline_pts : list (str)
        List of baseline correction points.
    toluene_pks : list (str)
        List of toluene peak positions.

    Returns
    -------
    None
    """
    with open(LOG_FILE, 'w') as file:
        json.dump({"baseline_pts": baseline_pts,
                  "toluene_pks": toluene_pks}, file)

    return None


def get_user_inputs():
    """Prompt user for baseline correction points and toluene peaks,
    with the option to reuse values from last session.

    Returns
    -------
    baseline_pts, toluene_pks : tuple (int, float)
        Baseline correction points and toluene reference peaks.
    """
    last_values = load_log()

    # baseline points
    if last_values["baseline_pts"]:
        print(f"Last used baseline points: {last_values['baseline_pts']}")
        use_last = input(
            "Use these baseline points? (y/n): ").strip().lower() == 'y'
        baseline_pts = last_values["baseline_pts"] if use_last else None

    else:
        baseline_input = input("Enter baseline correction points: ").strip()
        baseline_input = baseline_input.replace(",", " ")
        baseline_pts = list(map(int, baseline_input.split()))

    # toluene peaks
    if last_values["toluene_pks"]:
        print(f"Last used toluene peaks: {last_values['toluene_pks']}")
        use_last = input(
            "Use these toluene peaks? (y/n): ").strip().lower() == 'y'
        toluene_pks = last_values["toluene_pks"] if use_last else None


    else:
        toluene_input = input("Enter toluene peaks (pixels): ").strip()
        toluene_input = toluene_input.replace(",", " ")
        toluene_pks = list(map(float, toluene_input.split()))

    save_log(baseline_pts, toluene_pks)

    return baseline_pts, toluene_pks


def get_spectra_files(spectra_path):
    """Get a list of spectra files in directory.

    Parameters
    ----------
    spectra_path : str
        Path to the directory containing spectra files.

    Returns
    -------
    spectra_files : list (str)
        List of spectra file names.
    """
    spectra_files = [file for file in os.listdir(
        spectra_path) if file.endswith(".txt")]

    return spectra_files


def load_spectra(spectra_files):
    """Load spectra data into a numpy array.

    Parameters
    ----------
    spectra_files : list (str)
        List of spectra file names.

    Returns
    -------
    spectra_data : np.array
        Array of spectra data with shape (pixels, files + 1).
    """
    pixel_count = sum(1 for _ in open(spectra_files[0]))
    spectra_data = np.zeros((pixel_count, len(spectra_files) + 1))

    for idx, spectra in enumerate(spectra_files):
        with open(spectra, 'r') as file:
            spectra_data[:, idx] = [float(line.strip().split(',')[-1])
                                    for line in file.readlines()]

    return spectra_data


def baseline_correct(spectra_data, baseline_pts):
    """Perform baseline correction on the spectra data.

    Parameters
    ----------
    spectra_data : np.array
        Array of spectra data with shape (pixels, files + 1).
    baseline_pts : list (int)
        Baseline correction points.

    Returns
    -------
    spectra_data : np.array
        Baseline corrected array of spectra data with shape (pixels, files + 1).
    """
    # exclude last column - used for mean spectrum
    baselines = spectra_data[baseline_pts, :-1]
    interpolated_baseline = np.array(
        [np.interp(range(len(spectra_data)), baseline_pts, baselines[:, idx])
         for idx in range(baselines.shape[1])]).T

    spectra_data[:, :-1] -= interpolated_baseline

    return spectra_data


def remove_cosmic_rays(spectra_data):
    """Remove cosmic rays from the spectra data.

    Parameters
    ----------
    spectra_data : np.array
        Baseline corrected array of spectra data with shape (pixels, files + 1).

    Returns
    -------
    spectra_data : np.array
        Baseline and cosmic ray corrected array of spectra data with shape (pixels, files + 1).
    """
    # exclude last column - used for mean spectrum
    mean_values = np.mean(spectra_data[:, :-1], axis=1)
    std_devs = np.std(spectra_data[:, :-1], axis=1)

    # identify cosmic rays and replace value with average value at pixel
    cosmic_mask = spectra_data[:, :-1] >= \
        (mean_values[:, None] + std_devs[:, None])
    spectra_data[:, :-1][cosmic_mask] = np.broadcast_to(mean_values[:, None], spectra_data[:, :-1].shape)[cosmic_mask]

    # save mean spectrum
    spectra_data[:, -1] = mean_values

    return spectra_data


def toluene_correction(toluene_pks):
    """Use toluene to calculate the corresponding wavenumber values
    for each pixel.

    Parameters
    ----------
    toluene_peaks : list (float)
        Pixel numbers of the toluene reference peaks.

    Returns
    -------
    slope, intercept : tuple (float)
        Slope and intercept for toluene correction.
    """
    x = np.array(toluene_pks)
    y = np.array([1003.1, 1030.1, 1210.0, 1378.6, 1604.1])
    slope, intercept = np.linalg.lstsq(
        np.vstack([x, np.ones(len(x))]).T, y, rcond=None)[0]

    return slope, intercept


def save_corrected_spectra(spectra_files, spectra_data, slope, intercept):
    """Save corrected spectra files and averaged corrected spectrum.

    Parameters
    ----------
    spectra_files : list (str)
        List of spectra file names.
    spectra_data : np.array
        Baseline and cosmic ray corrected array of spectra data with shape (pixels, files + 1).
    slope : float
        Slope of the toluene correction.
    intercept : float
        Intercept of the toluene correction.

    Returns
    -------
    None
    """
    # convert pixels to wavenumbers
    pixels = np.arange(len(spectra_data))
    wavenumbers = pixels * slope + intercept

    # save individual corrected spectra
    for spectra_idx, spectrum in enumerate(spectra_files):
        spectrum_corrected = spectrum.replace('.txt', '-corrected.dat')
        with open(spectrum_corrected, 'w') as file:
            for row, wavenumber in enumerate(wavenumbers):
                file.write(f"{wavenumber:.4f}    {spectra_data[row, spectra_idx]:.6f}\n")

    # Save averaged corrected spectrum
    spectrm_average = 'averaged_corrected_spectrum.dat'
    with open(spectrm_average, 'w') as file:
        for row, wavenumber in enumerate(wavenumbers):
            file.write(f"{wavenumber:.4f}    {spectra_data[row, -1]:.6f}\n")


def main():
    """Main Program."""
    # get user inputs
    baseline_points, toluene_peaks = get_user_inputs()

    # get spectra files, load, and baseline correct
    spectra_files = get_spectra_files(os.getcwd())
    spectra_data = load_spectra(spectra_files)
    corrected_data = baseline_correct(spectra_data, baseline_points)

    # remove cosmic rays and apply toluene correction
    cleaned_data = remove_cosmic_rays(corrected_data)
    slope, intercept = toluene_correction(toluene_peaks)

    # save processed spectra
    save_corrected_spectra(spectra_files, cleaned_data, slope, intercept)


if __name__ == "__main__":
    main()

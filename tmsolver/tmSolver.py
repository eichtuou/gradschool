"""This script solves the protein correlation time tau_m (tm) from the
Model-Free Analysis (MFA). It uses two spectral density functions (J)
from DOI:10.1007/s10858-007-9214-2

    Equation 2: Spectral density function without slow or fast motions
        J( %omega ) = frac{2}{5} %tau_m (
            ( frac{ S_2 }{ 1 + (%omega %tau_m)^2 })
            + ( frac{ (1 - S_2)(%tau_e + %tau_m)%tau_e }
                { (%tau_e + %tau_m)^2 + (%omega %tau_e %tau_m)^2 })
        )

    Equation 3: Spectral density function with slow or fast motions
        J( %omega ) = frac{ 2 }{ 5 } %tau_m (
            ( frac{ S_2 }{ 1 + (%omega %tau_m)^2 } )
            + (frac { (1 - S_f)(%tau_f + %tau_m) %tau_f }{
                (%tau_f + %tau_m)^2 + (%omega %tau_f %tau_m)^2 } )
            + (frac { (S_f - S_2)(%tau_s + %tau_m) %tau_s }{
                (%tau_s + %tau_m)^2 + (%omega %tau_s %tau_m)^2 } )
         )
"""

import os
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
        description="Solves the protein correlation time (tm) from the Model-Free Analysis J(0) results.")
    parser.add_argument(
        "j0_file",
        type=str,
        help="Path to the input J(0) results file.")

    args = parser.parse_args()

    if not args.j0_file.endswith(".dat"):
        parser.error("Input file must be in DAT format.")
    if not os.path.isfile(args.j0_file):
        parser.error(f"File not found: {args.j0_file}")


    return args


def get_mfa(j0_file):
    """Get MFA data for each residue.

    Parameters
    ----------
    j0_file : str
        Path to the J(0) results file.

    Returns
    -------
    mfa_data : dict
        Dictionary containing the MFA results for each residue.
        Keys : resid, j0, s2, s2_f, s2_s, tau_e, tau_f, tau_s
    """
    data = []
    with open(j0_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            data.append(line.split())

    data = np.array(data, dtype=float)
    mfa_data = {
        "resid": data[:, 0].astype(int),
        "j0": data[:, 1],
        "s2": data[:, 2],
        "s2_f": data[:, 3],
        "s2_s": data[:, 4],
        "tau_e": data[:, 5],
        "tau_f": data[:, 6],
        "tau_s": data[:, 7],
    }

    return mfa_data


def taum_eqn2(j0, s2, tau_e):
    """Tau_m [s] value calculated from the spectral density function without slow or fast motions.

    Parameters
    ----------
    j0 : float
        Spectral density at the 0 frequency, J(0).
    s2 : float
        Generalized order parameter.
    tau_e : float
        Effective correlation time associated with the rate of the motion of
        individual bond vectors.

    Returns
    ----------
    tau_m : float
        Calculated value of tau_m with given parameters.
    """
    a = -0.4 * s2
    b = j0 - 1.2 * s2 * tau_e - 0.4 * tau_e
    c = 2.0 * j0 * tau_e - 0.4 * tau_e**2
    d = j0 * tau_e**2

    tau_m = np.roots([a, b, c, d])
    tau_m = tau_m[np.isreal(tau_m) & (tau_m > 0)].real
    tau_m = tau_m[0] if tau_m.size > 0 else np.nan

    return tau_m


def taum_eqn3(j0, s2, s2_f, tau_f, tau_s):
    """Tau_m [s] value calculated from the spectral density function with slow or fast motions.

    Parameters
    ----------
    j0 : float
        Spectral density at the 0 frequency, J(0).
    s2 : float
        Generalized order parameter.
    s2_f : float
        Generalized order parameter of bond vectors that undergo fast motions.
    s2_s : float
        Generalized order parameter of bond vectors that undergo slow motions.
    tau_f : float
        Effective correlation time associated with the rate of the motion of
        individual bond vectors that undergo fast motions.
    tau_s : float
        Effective correlation time associated with the rate of the motion of
        individual bond vectors that undergo slow motions.

    Returns
    ----------
    tau_m : float
        Calculated value of tau_m with given parameters.
    """
    a = -0.4 * s2
    b = j0 - 1.2 * s2 * tau_s - 0.4 * s2_f * tau_s - \
        0.4 * tau_f - 0.8 * s2 * tau_f + 0.4 * s2_f * tau_f
    c = 2.0 * j0 * tau_s - 0.8 * s2 * (tau_s**2) + 0.4 * s2_f * (tau_s**2) + 2 * j0 * tau_f - 0.4 * (tau_f**2) - 0.4 * s2 * (
        tau_f**2) + 0.4 * s2_f * (tau_f**2) - 0.8 * tau_s * tau_f - 1.6 * s2 * tau_s * tau_f + 1.6 * s2_f * tau_s * tau_f
    d = j0 * (tau_s**2) + j0 * (tau_f**2) + 4 * j0 * tau_s * tau_f - 0.4 * (tau_s**2) * tau_f - 1.6 * s2 * (tau_s**2) * tau_f + \
        1.2 * s2_f * (tau_s**2) * tau_f - 0.8 * tau_s * (tau_f**2) - 1.2 * s2 * tau_s * (tau_f**2) + 1.2 * s2_f * tau_s * (tau_f**2)
    e = 2 * j0 * tau_s * (tau_f**2) + 2 * j0 * (tau_s**2) * tau_f - 0.4 * (tau_s**2) * (
        tau_f**2) - 0.8 * s2 * (tau_s**2) * (tau_f**2) + 0.8 * s2_f * (tau_s**2) * (tau_f**2)
    f = j0 * (tau_s**2) * (tau_f**2)

    tau_m = np.roots([a, b, c, d, e, f])
    if tau_m.size == 0 or tau_m[0] == 0:
        tau_m = np.nan
    else:
        tau_m = tau_m[0]

    return tau_m


def get_tau(mfa_data):
    """Get tau_m for each residue using Equations 2 and 3.

    Parameters
    ----------
    mfa_data : dict
        Dictionary containing the MFA results for each residue.
        Keys : resid, j0, s2, s2_f, s2_s, tau_e, tau_f, tau_s

    Returns
    -------
    tau_eq2 : list (float)
        tau_m values calculated from Equation 2.
    tau_eq3 : list (float)
        tau_m values calculated from Equation 3.
    """
    tau_eq2 = []
    tau_eq3 = []

    for idx in range(len(mfa_data['resid'])):
        params_eq2 = [
            mfa_data['j0'][idx],
            mfa_data['s2'][idx],
            mfa_data['tau_e'][idx]
        ]
        params_eq3 = [
            mfa_data['j0'][idx],
            mfa_data['s2'][idx],
            mfa_data['s2_f'][idx],
            mfa_data['tau_f'][idx],
            mfa_data['tau_s'][idx]
        ]
        tau_eq2.append(taum_eqn2(*params_eq2))
        tau_eq3.append(taum_eqn3(*params_eq3))

    return tau_eq2, tau_eq3


def write_output(j0_file, tau_eq2, tau_eq3):
    """Write results to output file.

    Parameters
    ----------
    j0_file : str
        Path to the J(0) results file.
    tau_eq2 : list (float)
        tau_m values calculated from Equation 2.
    tau_eq3 : list (float)
        tau_m values calculated from Equation 3.

    Returns
    -------
    None
    """
    output_file_1 = f"{j0_file[:-4]}-tm-eqn2.out"
    output_file_2 = f"{j0_file[:-4]}-tm-eqn3.out"

    with open(output_file_1, "w") as file:
        file.write(
            f"tau_m [s] values calculated with no fast or slow motions\n")
        file.write(f"Average: {np.nanmean(tau_eq2):.6e}\n")
        file.write(f"Std Dev: {np.nanstd(tau_eq2):.6e}\n\n")
        for idx in range(len(tau_eq2)):
            file.write(f"residue {idx + 1} = {tau_eq2[idx]:.6e}\n")

    with open(output_file_2, "w") as file:
        file.write(f"tau_m [s] values calculated with fast and slow motions\n")
        file.write(f"Average: {np.nanmean(tau_eq3):.6e}\n")
        file.write(f"Std Dev: {np.nanstd(tau_eq3):.6e}\n\n")
        for idx in range(len(tau_eq3)):
            file.write(f"residue {idx + 1} = {tau_eq3[idx]:.6e}\n")

    return None


def main():
    """Main Program."""
    args = parse_arguments()
    mfa_data = get_mfa(args.j0_file)
    tau1, tau2 = get_tau(mfa_data)
    write_output(args.j0_file, tau1, tau2)


if __name__ == "__main__":
    main()

"""This script generates input files and submission scripts for IETsim cubebuilder."""

import os
import argparse
import textwrap


def parse_arguments():
    """Validate input arguments

    Returns
    ----------
    args : argparse obj
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate cube calculation and submission scripts.")
    parser.add_argument("molecule", type=str, help="Molecule name.")
    parser.add_argument("--orbital", type=str, default="L2",
                        help="Orbital name (default: L2).")
    parser.add_argument("--time_fs", type=int, default=50,
                        help="Total time in femtoseconds (default: 50).")

    return parser.parse_args()


def generate_input_script(cubefile, timestep):
    """Generate a cube calculation input script.

    Parameters
    ----------
    cubefile : str
        Name of the cube input script.
    timestep : int
        Time step index.

    Returns
    -------
    None
    """
    buffer = textwrap.dedent(f"""\
        region
        0.25
        0.0000  15.24749188
        0.0000  10.48704607
        0.0000  26.00000000

        name
        {cubefile[:-3]}

        make
        1
        {timestep}
    """)

    with open(cubefile, 'w') as file:
        file.write(buffer)
    os.chmod(cubefile, 0o755)

    return None


def generate_submission_script(subfile, cubefile, wavefile):
    """Generate a submission script for the cube job.

    Parameters
    ----------
    subfile : str
        Name of the submission script.
    cubefile : str
        Name of the cube input script.
    wavefile : str
        Name of the wave file.

    Returns
    -------
    None
    """
    buffer = textwrap.dedent(f"""\
        #!/usr/bin/bash
        #BSUB -R span[ptile=8]
        #BSUB -R "model != L5535"
        #BSUB -R "mem>24100"
        #BSUB -q cos
        #BSUB -W 24:00
        #BSUB -n 2
        #BSUB -J {cubefile[:-3]}
        #BSUB -o output
        #BSUB -e error

        echo jobid = $LSB_JOBID
        echo hosts = $LSB_HOSTS

        date
        cubebuilder {cubefile} {wavefile}
        date
    """)

    with open(subfile, 'w') as file:
        file.write(buffer)
    os.chmod(subfile, 0o755)

    return None


def generate_all_scripts(cubename, wavefile, time_fs):
    """
    Process time steps to generate cube and submission scripts.

    Parameters
    ----------
    cubename : str
        Base name for cubefiles.
    wavefile : str
        Name of wave file.
    time_fs : int
        Total simulation time in femtoseconds.

    Returns
    -------
    None
    """
    submission_commands = []

    for timestep in range(0, time_fs + 10, 10):

        if timestep == 0:
            timestep += 1

        # generate input and submission scripts
        cubefile = f"{cubename}_{timestep}.in"
        subfile = f"subcube_{cubefile[:-3]}"
        generate_input_script(cubefile, timestep)
        generate_submission_script(subfile, cubefile, wavefile)

        # record command for batch submission
        submission_commands.append(f"bsub < {subfile}")

    # batch submission script
    batchfile = 'submit_batch.sh'
    with open(batchfile, 'w') as file:
        for command in submission_commands:
            file.write(f"{command}\n")
    os.chmod(batchfile, 0o755)

    return None


def main():
    """Main Program."""
    args = parse_arguments()

    molecule = args.molecule
    orbital = args.orbital
    time_fs = args.time_fs
    cubename = f"{molecule}_{orbital}_cube"
    wavefile = f"{molecule}_aligned.bind.edyn.wave"

    generate_all_scripts(cubename, wavefile, time_fs)


if __name__ == "__main__":
    main()

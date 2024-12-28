"""This script generates TD-DFT input files from a DFTB conformation scan
output. It also generates submission scripts for each TD-DFT calculation,
and an input stream file to submit all the jobs at once.
"""

import os
import shutil as sh
import textwrap
from typing import List

# --------------------USER INPUT SECTION------------------------!
CLUSTER = 'henry'                   # Options: 'henry', 'murgas'
QUEUE = 'single_chassis'            # Name of the queue
PREFIX = 'dmonoCA_slab_tarj_'       # Complex name
# --------------------------------------------------------------!


def get_input_files(prefix: str) -> List[str]:
    """Get all input files matching the specified prefix."""
    input_files = [file for file in os.listdir(
        os.getcwd()) if prefix in file and file.endswith('.com')]

    return input_files


def get_coordinates(input_file: str) -> str:
    """Get coordinates from input file."""
    with open(input_file, 'r') as file:
        buffer = file.read().split('\n\n')
        coordinates = '\n'.join(buffer[2].split('\n')[1:]) + '\n\n'

    return coordinates


def get_header(job_name: str) -> str:
    """Generate header for the new input file."""
    header = textwrap.dedent(f"""\
        %chk={job_name}.chk
        %mem=16GB
        %nprocshared=8
        # p b3lyp/gen
            empiricaldispersion=gd2
            pseudo=cards
            integral=ultrafine
            td(singlets,nstates=30)
            scrf(pcm,solvent=water,read)
            nosymm

        {job_name}

        -2 1
    """)

    return header


def get_basis_set() -> str:
    """Generate basis set for the new input file."""
    basis_set = textwrap.dedent(f"""\
        C H N O 0
        6-311g*
        ****
        Fe 0
        SDD
        F   1   1.00
              2.462
        ****
        FE 0
        SDD
    """)

    return basis_set


def write_input_file(file_name: str, header: str,
                     coordinates: str, basis_set: str) -> None:
    """Create a new input file with header, coordinates, and basis set."""
    sh.move(file_name, file_name + '~')

    with open(file_name, 'w') as file:
        file.write(header)
        file.write(coordinates)
        file.write(basis_set)

    return None


def generate_submission_script(
    cluster: str,
    queue: str,
    file_name: str,
    script_name: str
) -> str:
    """Generate a submission script for the specified cluster and input file."""
    job_name = file_name[:-4]
    template = {
        'henry': textwrap.dedent(f"""\
            #!/usr/bin/bash
            #BSUB -R "model != L5535"
            #BSUB -R span[ptile=8]
            #BSUB -R "mem>16100"
            #BSUB -q {queue}
            #BSUB -n 8
            #BSUB -W 2:00
            #BSUB -J {job_name}
            #BSUB -o output
            #BSUB -e error

            echo jobid = $LSB_JOBID
            echo hosts = $LSB_HOSTS

            date
            g09 {file_name}
            date
        """),

        'murgas': textwrap.dedent(f"""\
            #!/bin/bash
            # These commands set up the Grid Environment for your job:
            #PBS -jeo
            #PBS -o output
            #PBS -e error
            #PBS -N {job_name}
            #PBS -l pmem=2GB,nodes=1:ppn=8,walltime=300:00:00

            RUNDIR=$PBS_O_WORKDIR
            export RUNDIR
            cd $RUNDIR

            date
            g09 {file_name}
            date
        """)
    }

    with open(script_name, 'w') as file:
        file.write(template[cluster])
    os.chmod(script_name, 0o755)

    submission_command = f"{
        'bsub <' if cluster == 'henry' else 'qsub'} {script_name}"

    return submission_command


def main() -> None:
    """Main program."""
    submission_commands = []
    basis_set = get_basis_set()
    com_files = get_input_files(PREFIX)

    for com_file in com_files:
        job_name = com_file[:-4]
        header = get_header(job_name)
        coordinates = get_coordinates(com_file)
        write_input_file(com_file, header, coordinates, basis_set)
        submission_commands.append(
            generate_submission_script(
                CLUSTER, QUEUE, com_file))

    with open('suball.sh', 'w') as file:
        file.write('\n'.join(submission_commands) + '\n')
    os.chmod('suball.sh', 0o755)

    return None


if __name__ == "__main__":
    main()

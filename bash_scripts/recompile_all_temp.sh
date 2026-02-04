#!/bin/bash

#SBATCH --partition=pm6-isw2,pm9-isw0,pm11-isw2,cn
#SBATCH --job-name=2001_to_2016
#SBATCH --account=ehpc-reg-2023r03-178
#SBATCH --qos=ehpc-reg-2023r03-178
#SBATCH --time=96:00:00

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-core=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=251G
#SBATCH -e job.%J.err
#SBATCH -o job.%J.out

#SBATCH --mail-type=ALL
#SBATCH --mail-user=m.c.boulogne@student.utwente.nl

source ~/.bash_shell

set -euo pipefail


# Compile once
CC99='mpicc -std=c99 -D_GNU_SOURCE' qcc -Wall -O2 -D_MPI=1 bubbleAtLubis.c -o bubbleAtLubis_mpi -lm -disable-dimensions
CC99='mpicc -std=c99 -D_GNU_SOURCE' qcc -Wall -O2 -D_MPI=1 bubbleAtLubisStokes.c -o bubbleAtLubisStokes_mpi -lm -disable-dimensions
CC99='mpicc -std=c99 -D_GNU_SOURCE' qcc -Wall -O2 -D_MPI=1 bubbleAtLubis_unaltered_3phase.c -o bubbleAtLubis_unaltered_3phase_mpi -lm -disable-dimensions

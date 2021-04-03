#!/bin/bash
#
#SBATCH --job-name=2Cr0.2
#SBATCH --output=2Cr0.2.out
#SBATCH -N 1
#SBATCH --ntasks-per-node=48
#SBATCH --time=10:00:00
#SBATCH -p debug

EXEC=/home/sf05/q-e-qe-6.7MaX-Release/bin/pw.x

mpirun -np 48 $EXEC -inp 2Cr0.2.scf.in > 2Cr0.2.scf.out
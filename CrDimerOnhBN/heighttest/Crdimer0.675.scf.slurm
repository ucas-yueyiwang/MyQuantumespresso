#!/bin/bash
#
#SBATCH --job-name=Crdimer0.675
#SBATCH --output=Crdimer0.675.out
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH --time=10:00:00
#SBATCH -p debug

EXEC=/home/yueyi/q-e-gpu-qe-gpu-6.7/bin/pw.x

mpirun -np 16 $EXEC -inp Crdimer0.675.scf.in > Crdimer0.675.scf.out

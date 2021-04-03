#!/bin/bash
#
#SBATCH --job-name=Crdimer0.69
#SBATCH --output=Crdimer0.69.out
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH --time=00:30:00
#SBATCH -p debug

EXEC=/home/yueyi/q-e-gpu-qe-gpu-6.7/bin/pw.x

mpirun -np 16 $EXEC -inp Crdimer0.69.scf.in > Crdimer0.69.scf.out

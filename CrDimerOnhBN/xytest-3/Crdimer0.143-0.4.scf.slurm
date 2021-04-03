#!/bin/bash
#
#SBATCH --job-name=Crdimer0.143-0.4
#SBATCH --output=Crdimer0.143-0.4.out
#SBATCH -N 1
#SBATCH --ntasks-per-node=48
#SBATCH --time=10:00:00
#SBATCH -p debug

EXEC=/home/sf05/q-e-qe-6.7MaX-Release/bin/pw.x

mpirun -np 48 $EXEC -inp Crdimer0.143-0.4.scf.in > Crdimer0.143-0.4.scf.out
        
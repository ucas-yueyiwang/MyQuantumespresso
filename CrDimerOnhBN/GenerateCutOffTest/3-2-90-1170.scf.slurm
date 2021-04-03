#!/bin/bash
#SBATCH -J 3-2-90-1170
#SBATCH -p regular
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o 3-2-90-1170.out

module load mpi/intelmpi/2017.4.239
srun --mpi=pmi2 /public/software/apps/qe/6.4.1/intelmpi/bin/pw.x < 3-2-90-1170.scf.in > 3-2-90-1170.scf.out

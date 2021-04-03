#!/bin/bash
#SBATCH -J 3TNCrhBN
#SBATCH -p regular
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o 3TNCrhBN.out

module load mpi/intelmpi/2017.4.239
srun --mpi=pmi2 /public/software/apps/qe/6.4.1/intelmpi/bin/pw.x < 3TNCrhBN.relax.in > 3TNCrhBN.relax.out

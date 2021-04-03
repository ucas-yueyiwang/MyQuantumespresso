#!/bin/bash
#SBATCH -J 3TBCrhBN
#SBATCH -p regular
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o 3TBCrhBN.out

module load mpi/intelmpi/2017.4.239
srun --mpi=pmi2 /public/software/apps/qe/6.4.1/intelmpi/bin/pw.x < 3TBCrhBN.relax.in > 3TBCrhBN.relax.out

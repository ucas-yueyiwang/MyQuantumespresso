#!/bin/bash
#SBATCH -J HNBCrhBN
#SBATCH -p regular
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -o HNBCrhBN.out

module load mpi/intelmpi/2017.4.239
srun --mpi=pmi2 /public/software/apps/qe/6.4.1/intelmpi/bin/pw.x < HNBCrhBN.relax.in > HNBCrhBN.relax.out

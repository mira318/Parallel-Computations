#!/bin/bash
#
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=RT_study
#SBATCH --job-name=trying_job
#SBATCH --comment="Run mpi from config"
#SBATCH --output=out_multi.txt
#SBATCH --error=error.txt
#SBATCH --input=input.txt
#SBATCH --open-mode=append
mpiexec ./a.out

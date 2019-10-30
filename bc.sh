#!/bin/bash

#SBATCH --chdir /scratch/felisaz
#SBATCH --array=10,15,20,25,30

mkdir -p data

XDIR=~/monte-carlo
BIN=$XDIR/sim
CONFIG=$XIR/config_bc.in

# Run the simulation with each given N
echo "$BIN $CONFIG N=$SLURM_TASK_ID filename=data/$SLURM_ARRAY_TASK_ID.out"


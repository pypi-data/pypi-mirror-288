#!/bin/bash
#SBATCH --job-name=nestml_benchmark
#SBATCH --account=slns
#SBATCH --partition=dc-cpu
#SBATCH --time=01:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=64
#SBATCH --hint=nomultithread
#SBTACH --exclusive
#SBATCH --output=run_simulation_aeif_psc_alpha_neuron_Nestml_Plastic__with_stdp_synapse_Nestml_Plastic_2_1_%j.out
#SBATCH --error=run_simulation_aeif_psc_alpha_neuron_Nestml_Plastic__with_stdp_synapse_Nestml_Plastic_2_1_%j.err
#SBATCH --disable-perfparanoid

export OMP_PROC_BIND=TRUE
export PROGRAM="python3 examples/brunel_alpha_nest.py --simulated_neuron aeif_psc_alpha_neuron_Nestml_Plastic__with_stdp_synapse_Nestml_Plastic --network_scale 20000 --nodes 2 --threads 128  --iteration 1 --benchmarkPath /p/project1/cslns/babu1/nestml/extras/benchmark/Running/../Output_MPI/aeif_psc_alpha/timings_strong_scaling_mpi --rng_seed 2099828418"
srun $PROGRAM
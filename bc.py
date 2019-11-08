#!/bin/python3
# A script to find the smallest system so that side effects are
# negligible

import numpy as np
import os

# Generate all files to run each simulation in the scratch directory

# Run each sim within a sbatch

# Retreve and analyse data

Ns = np.array([10, 15, 20, 30])
extra_flags = ""

config = "~/monte-carlo/config_bc.in"
sim_bin = "~/monte-carlo/sim"

workdir = os.path.abspath("monte-carlo/") + "/"


# Reset everything
os.system("rm -rdf {}".format(workdir))
os.system("mkdir -p {}".format(workdir))


print("Generating and running scripts ...\n")
for N in Ns:
    prefix = "{}sim_{}/".format(workdir, N)
    os.system("mkdir {}".format(prefix))

    with open(prefix + "sim.sh", "w") as f:
        f.write("""#!/bin/bash -l
        #SBATCH --job-name=sim_N_{}
        #SBATCH --time=0-01:00
        {} {} "N={}" {}""".format(N, sim_bin, config, N, extra_flags))
    
    os.system("cd {} && sbatch sim.sh && cd {}".format(prefix, workdir))

print("Done. ")

#!/bin/python3
"""A script to start several simulations with different values for
H. The T scanning will already be done by the annealing. Very similar
to bc.py.

"""

import numpy as np
import os

# Generate all files to run each simulation in the scratch directory

# Run each sim within a sbatch

# Retreve and analyse data

Hs = np.array([0, 1, 2, 3, 4, 5])
extra_flags = ""

config = "~/monte-carlo/config_grid.in"
sim_bin = "~/monte-carlo/sim_anneal"

workdir = os.path.abspath("monte-carlo_grid/") + "/"


# Reset everything
os.system("rm -rdf {}".format(workdir))
os.system("mkdir -p {}".format(workdir))


print("Generating and running scripts ...\n")
for H in Hs:
    prefix = "{}sim_{}/".format(workdir, H)
    os.system("mkdir {}".format(prefix))

    with open(prefix + "sim.sh", "w") as f:
        f.write("""#!/bin/bash -l
        #SBATCH --job-name=sim_H_{}
        #SBATCH --time=1:00:00
        {} {} "N={}" {}""".format(N, sim_bin, config, N, extra_flags))
    
    os.system("cd {} && sbatch sim.sh && cd {}".format(prefix, workdir))

print("Done. ")

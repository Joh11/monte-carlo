#!/bin/python3
# A script to find the smallest system so that side effects are
# negligible

import numpy as np
import os
import matplotlib.pyplot as plt

# Generate all files to run each simulation in the scratch directory

# Run each sim within a sbatch

# Retreve and analyse data

Ns = np.array([10, 15, 20, 30])
extra_flags = ""

config = "~/monte-carlo/config_bc.in"
sim_bin = "~/monte-carlo/sim"

workdir = "tmp/"


# Reset everything
os.system("rm -rdf {}".format(workdir))
os.system("mkdir -p {}".format(workdir))


print("Generating and running scripts ...\n")
for N in Ns:
    prefix = "{}sim_{}/".format(workdir, N)
    os.system("mkdir {}".format(prefix))

    with open(prefix + "sim.sh", "w") as f:
        f.write("""#!/bin/bash
        {} {} "N={}" {}""".format(sim_bin, config, N, extra_flags))
    

print("Waiting for the scripts to run ...")
with open(workdir + "wait.sh", "w") as f:
    f.write("""#!/bin/bash
echo "All jobs done" """)
    
os.system("sbatch -w --dependency $(sqeue -u felisaz --noheader --name sim.sh --format %i) {}".format(workdir + "wait.sh"))


print("Analysing the data ...")
datas = []
for N in Ns:
    prefix = "{}sim_{}/".format(workdir, N)
    data = np.loadtxt(prefix + "data.out")
    datas.append(data[:, 0:3]) # steps, E, and Mx

plt.figure()
for data, N in zip(datas, Ns):
    plt.subplot(1, 2, 1)
    plt.plot(data[:, 0], data[:, 1], label="N={}".format(N))
    plt.subplot(1, 2, 2)
    plt.plot(data[:, 0], data[:, 2], label="N={}".format(N))

plt.legend()

plt.subplot(1, 2, 1)
plt.xlabel("steps")
plt.ylabel("E")

plt.subplot(1, 2, 2)
plt.xlabel("steps")
plt.ylabel("Mx")

plt.show()

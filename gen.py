"""A file to run simulations and generate the hdf5 dataset"""

import numpy as np
from os import system
import h5py

# Hs = np.array([0.1, 0.2,
#                1, 1.1,
#                2, 2.1,
#                3, 3.1])
Hs = np.array([0])
Ts = np.linspace(0.1, 2, 200)

config = "config/big.in"
outdir = "data/big/"
Nanneal = 5000

outfile = outdir + "out"
statefile = outdir + "state"

Nsample = 10
samples = ["sample_{}".format(i+1) for i in range(Nsample)]

with h5py.File("dataset0.hdf5", "w") as f:
    f.attrs["config"] = config
    f.attrs["Nanneal"] = Nanneal
    for sample in samples:
        for H in Hs:
            print("Starting H={} ...".format(H))
            grp = f.require_group("H={}".format(H))
            grp.attrs["H"] = H
            
            # First step
            grp2 = grp.require_group("T={}".format(Ts[0]))
            grp2.attrs["T"] = Ts[0]
            # Run the simulation
            system("./sim {} \"filename={}\" \"temperature={}\" \"H=(0 0 {})\" \"outstate={}\""
                   .format(config, outfile, Ts[0], H, statefile))
            # Store data
            data = np.loadtxt(outfile)
            dset = grp2.create_dataset(sample, data=data)
            dset.attrs["E"] = np.mean(data[:, 5])
            dset.attrs["varE"] = np.var(data[:, 5])
            dset.attrs["M"] = np.mean(data[:, 8])
            dset.attrs["varM"] = np.var(data[:, 8])
            # Clear temporary files
            system("rm {}".format(outfile))
            
            # Then annealing
            for T in Ts[1:]:
                print("Starting T={} ...".format(T))
                grp2 = grp.require_group("T={}".format(T))
                grp2.attrs["T"] = T
                
                # Run the simulation
                system("./sim {} \"filename={}\" \"temperature={}\" \"H=(0 0 {})\" \"outstate={}\" \"instate={}\" \"Nthermal={}\" "
                       .format(config, outfile, T, H, statefile, statefile, Nanneal))
                # Store data
                data = np.loadtxt(outfile)
                dset = grp2.create_dataset(sample, data=data)
                dset.attrs["E"] = np.mean(data[:, 5])
                dset.attrs["varE"] = np.var(data[:, 5])
                dset.attrs["M"] = np.mean(data[:, 8])
                dset.attrs["varM"] = np.var(data[:, 8])
                # Clear temporary files
                system("rm {}".format(outfile))


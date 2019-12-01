"""A program to scan a grid in T space"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from os import system
import os

Ns = np.array([10, 20, 30, 40, 50])

cfgfile = "config/bc.in"
outdir  = "data/scanN/high/"

def make_filename(N):
    return outdir + "scan_{}.out".format(N)

def run_sim():
    for N in Ns:
        f = make_filename(N)
        if os.path.exists(f):
            print("Skipped N={}".format(N))
        else:
            system("./sim {} \"filename={}\" \"N={}\" ".format(cfgfile,
                                                               f, N))

def analysis():
    Es = []
    for N in Ns:
        data = np.loadtxt(make_filename(N))
        Ez = data[:, -4]
        Es.append(Ez)

    plt.figure()
    for N, E in zip(Ns, Es):
        plt.plot(np.arange(E.shape[0]), E, label="N={}".format(N))
    plt.xlabel("iteration step")
    plt.ylabel("E per site")
    plt.legend()
    plt.show()

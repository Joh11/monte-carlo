"""A program to scan a grid in H-T space, using annealing in the T direction"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from os import system, path

Hs = np.linspace(0, 5, 20)
Ts = np.linspace(0, 4, 20)

cfgfile = "config/scan.in"
outdir  = "data/scan/"

def make_filename(H, T):
    return outdir + "scan_{}_{}.out".format(H, T)

def run_sim():
    statefile = outdir + "annealing.state"
    for H in Hs:
        firstpass=True
        for T in Ts:
            f = make_filename(H, T)
            if firstpass: # Do not load from the state file
                system("./sim {} \"filename={}\" \"temperature={}\" \"H=(0 0 {})\" \"outstate={}\""
                       .format(cfgfile, f, T, H, statefile))
                firstpass = False

            if path.exists(f):
                print("Skipped H={}, T={}".format(H, T))
            else:
                system("./sim {} \"filename={}\" \"temperature={}\" \"H=(0 0 {})\" \"outstate={}\" \"instate={}\" \"Nthermal=100\" "
                       .format(cfgfile, f, T, H, statefile, statefile))

def rescale(s, H, T):
    # critical exponents and temperature (theoretical ones)
    beta = 0.365
    gamma = 1.39
    delta = 4.8
    Tc = 0.75

    epsilon = (T - Tc) / Tc
    x = epsilon ** (gamma + beta) / H
    y = s * (1 - 1 / delta)

    return x, y

def analysis():
    shape = (len(Hs), len(Ts))
    Harr = np.zeros(shape)
    Tarr = np.zeros(shape)
    Marr = np.zeros(shape)
    susc_fluct = np.zeros(shape)
    
    for i, H in enumerate(Hs):
        for j, T in enumerate(Ts):
            data = np.loadtxt(make_filename(H, T))
            Mz = np.mean(data[:, -1])
            Harr[i, j] = H
            Tarr[i, j] = T
            Marr[i, j] = Mz
            if not T == 0:
                M = data[:, -1]
                susc_fluct[i, j] = (np.mean(M * M) - np.mean(M) ** 2) / T # we assumed kb = 1
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_wireframe(Harr, Tarr, Marr, color='green')
    ax.set_xlabel('H')
    ax.set_ylabel('T')
    ax.set_zlabel('M_z per site')

    # We want to show every plot at once
    plt.figure()
    for H in Hs:
        Mzs = []
        for T in Ts:
            data = np.loadtxt(make_filename(H, T))
            Mzs.append(np.mean(data[:, -1]))
        plt.plot(Ts, np.array(Mzs), label="H={}".format(H))
    
    plt.xlabel("T []")
    plt.ylabel("Mz per site []")

    # We want to compute the susceptibility, i.e. the derivative of M
    # wrt H
    Hdiff = np.diff(Harr, axis=0)
    susc = np.diff(Marr, axis=0) / Hdiff
    Harr_half = (Harr[:-1, :] + Harr[1:, :]) / 2
    Tarr_half = (Tarr[:-1, :] + Tarr[1:, :]) / 2

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_wireframe(Harr_half, Tarr_half, susc, color='green')
    ax.set_xlabel('H')
    ax.set_ylabel('T')
    ax.set_zlabel('susceptibility per site')

    plt.figure()
    for H, T, s in zip((Hs[:-1] + Hs[1:]) / 2, Tarr_half, susc):
        plt.plot(T, s, label="H={:.2}".format(H))

    plt.xlabel("T []")
    plt.ylabel("dm/dH []")
    plt.legend()

    plt.figure()
    for H, T, s in zip(Hs, Tarr, susc_fluct):
        plt.plot(T, s, label="H={:.2}".format(H))
    plt.xlabel("T []")
    plt.ylabel("dm/dH []")
    plt.legend()

    plt.figure()
    for H, T, s in zip((Hs[:-1] + Hs[1:]) / 2, Tarr_half, susc):
        x, y = rescale(s, H, T)
        plt.plot(x, y, label="H={:.2}".format(H))

    plt.xlabel("εˠ⁺ᵝ/H")
    plt.ylabel("χ/H^(1/̣δ-1)")
    plt.legend()

    plt.figure()
    for H, T, s in zip(Hs, Tarr, susc_fluct):
        x, y = rescale(s, H, T)
        plt.plot(x, y, label="H={:.2}".format(H))
    plt.xlabel("εˠ⁺ᵝ/H")
    plt.ylabel("χ/H^(1/̣δ-1)")
    plt.legend()
    plt.show()

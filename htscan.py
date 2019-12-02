"""A program to scan a grid in H-T space, using annealing in the T direction"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from os import system, path

from tscan import binning

Tc = 0.702

dH = 0.01 # The variation of H used to compute the derivative
Hs_mean = np.linspace(0.1, 5, 4)
reduced_Ts = np.logspace(-6, 0)
Ts = Tc * (1 + reduced_Ts)

# Add intermediate values of H for differentiation
dxs = np.array([[-0.5, 0.5]]).repeat(len(Hs_mean), axis=0)
Hs = np.column_stack([Hs_mean, Hs_mean]) + dxs * dH
Hs = Hs.reshape((-1,))

cfgfile = "config/scan.in"
outdir  = "data/scanHT/"

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

def rescale(s, H, epsilon):
    # critical exponents and temperature (theoretical ones)
    beta = 0.365
    gamma = 1.39
    delta = 4.8

    x = epsilon ** (gamma + beta) / H
    y = s * (1 - 1 / delta)

    return x, y

def susceptibility_from_fluctuation():
    kiss = np.zeros((len(Hs), len(Ts)))

    for i, H in enumerate(Hs):
        for j, T in enumerate(Ts):
            data = np.loadtxt(make_filename(H, T))
            Mz = np.mean(data[:, -1])
            kiss[i, j] = 1 / T  * (np.mean(Mz * Mz) - np.mean(Mz) ** 2)# we assumed kb = 1

    return kiss

def load_Mz():
    Mzss = np.zeros((len(Hs), len(Ts)))
    errs = np.zeros((len(Hs), len(Ts)))

    for i, H in enumerate(Hs):
        for j, T in enumerate(Ts):
            data = np.loadtxt(make_filename(H, T))
            Mzss[i, j], errs[i, j] = np.mean(data[:, -1]), np.std(data[:, -1])
    return Mzss, errs


def fluct_vs_diff():
    # Get the fluctuation susceptibility
    ki_fluct = susceptibility_from_fluctuation()
    ki_fluct = (ki_fluct[::2] + ki_fluct[1::2]) / 2

    # Get the susceptibility from differentiation
    Mzss, errs = load_Mz()
    ki_diff = (Mzss[1::2] - Mzss[::2]) / dH

    # First with one
    plt.figure()
    plt.scatter(Ts, ki_fluct[0], label="Fluctuation susceptibility")
    plt.errorbar(Ts, ki_diff[0], errs[0], label="Differentation susceptibility", fmt=".")

    print(ki_diff[0], ki_diff[-1])
    
    plt.legend()
    plt.xlabel("T")
    plt.ylabel("χ")

    # Then with all
    plt.figure()
    for i, H in enumerate(Hs_mean):
        # plt.scatter(Ts, ki_fluct[0], label="Fluctuation susceptibility - {:.2}".format(H))
        plt.plot(Ts, ki_diff[i], label="Differentation susceptibility - {:.2}".format(H))
    
    plt.legend()
    plt.xlabel("T")
    plt.ylabel("χ")

    # Then normalized version
    plt.figure()
    for i, H in enumerate(Hs_mean):
        # plt.scatter(Ts, ki_fluct[0], label="Fluctuation susceptibility - {:.2}".format(H))
        x, y = rescale(ki_diff[i], H, reduced_Ts)
        plt.scatter(x, y, label="Differentation susceptibility - {:.2}".format(H))

    plt.xscale('log')
    plt.legend()
    plt.xlabel("")
    plt.ylabel("")

    
    plt.show()

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

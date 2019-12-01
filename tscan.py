"""A program to scan a grid in T space"""

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from os import system
import os
from math import sqrt

extra_args = ""
H = 0
Ts = np.linspace(0.01, 2, 200)

cfgfile = "config/scan.in"
outdir  = "data/scanT/"

def make_filename(H, T):
    return outdir + "scan_{}_{}.out".format(H, T)

def run_sim():
    for T in Ts:
        f = make_filename(H, T)
        if os.path.exists(f):
            print("Skipped T={}".format(T))
        else:
            system("./sim {} \"filename={}\" \"temperature={}\" \"H=(0 0 {})\" {}".format(cfgfile,
                                                                                          f, T, H, extra_args))

def binning(M, nbins):
    M = np.reshape(M, (nbins, -1))
    mu_m = np.mean(M, axis=1)
    sd_m = np.std(M, axis=1)

    mu_global = np.mean(mu_m)
    SD = np.std(mu_m)

    return mu_global, SD / sqrt(nbins)

def loadMz():
    Mzs = []
    errs = []

    for T in Ts:
        data = np.loadtxt(make_filename(H, T))
        Mz, err = binning(data[:, -1], 10)
        Mzs.append(Mz)
        errs.append(err)

    Mzs = np.array(Mzs)
    errs = np.array(errs)

    return Mzs, errs

def plot_with_errs():
    Mzs, errs = loadMz()

    plt.figure()
    plt.errorbar(Ts, Mzs, errs, fmt='.')
    plt.xlabel("T")
    plt.ylabel("Mz per site")

    plt.figure()
    plt.scatter(Ts, errs)
    plt.ylim(bottom=0)
    plt.xlabel("T")
    plt.ylabel("Error on the estimator")
    
    plt.show()

def criticalScaling(Tmin=0.45 , Tmax=0.65):
    M, errs = loadMz()

    mask = (Ts >= Tmin) * (Ts <= Tmax)
    x = Ts[mask]
    y = M[mask]
    errs = errs[mask]
    
    fitfunc = lambda p, T: p[0] * ((p[1] - T) / p[1]) ** p[2]
    errfunc = lambda p, T, M, err: (fitfunc(p, T) - M) / err

    p0 = np.array([1., 0.8, 0.5]) # initial guess
    p1, success = optimize.leastsq(errfunc, p0[:], args=(x, y, errs))
    
    print(p1, success)

    plt.figure()
    plt.scatter(Ts, M, label="Simulated points")

    Tscale = np.linspace(Tmin, Tmax)
    plt.plot(Tscale, fitfunc(p1, Tscale), color='r', label="Fit : Tc = {:.3}, β = {:.3}".format(p1[1], p1[2]))
    
    plt.xlabel("T")
    plt.ylabel("m(T)")
    plt.legend()
    plt.show()

def analysis():
    Mzs = loadMz()
    plt.figure()
    plt.scatter(Ts, Mzs)
    plt.xlabel("Temperature")
    plt.ylabel("Mz per site")
    plt.show()

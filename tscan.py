"""A program to scan a grid in T space"""

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from os import system
import os
from math import sqrt

extra_args = ""
# For a general T scan
H = 0
Ts = np.linspace(0.01, 2, 100)

cfgfile = "config/scan.in"
outdir  = "data/scanT/"

# In depth scan
# H = 0
# Ts = np.linspace(0.70, 0.80, 20)

# cfgfile = "config/scan.in"
# outdir  = "data/scanTdepth/"
# extra_args = "N=40"

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

def loadMz(return_err=False):
    Mzs = []
    errs = []
    for T in Ts:
        data = np.loadtxt(make_filename(H, T))
        Mz = np.mean(data[:, -1])
        Mzs.append(Mz)
        if return_err:
            errs.append(np.std(data[:, -1]))

    if return_err:
        return np.array(Mzs), np.array(errs)
    return np.array(Mzs)

def loadM():
    Ms = []
    for T in Ts:
        data = np.loadtxt(make_filename(H, T))
        Mxyz = np.mean(data[:, 2:5], axis=0)
        M = sqrt(np.sum(Mxyz * Mxyz))
        Ms.append(M)

    return np.array(Ms)

def criticalScaling(Tmin=0.5 , Tmax=0.74):
    M, errs = loadMz(return_err=True)

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

def criticalScalingNoErr(Tmin=0.5 , Tmax=0.74):
    M = loadM()

    mask = (Ts >= Tmin) * (Ts <= Tmax)
    x = Ts[mask]
    y = M[mask]
    
    fitfunc = lambda p, T: p[0] * ((p[1] - T) / p[1]) ** p[2]
    errfunc = lambda p, T, M: (fitfunc(p, T) - M)

    p0 = np.array([1., 0.8, 0.5]) # initial guess
    p1, success = optimize.leastsq(errfunc, p0[:], args=(x, y))
    
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

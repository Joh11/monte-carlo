# A script to find the smallest system so that side effects are
# negligible

import numpy as np
import os
import matplotlib.pyplot as plt


# Tweakable params
T = 1

Ns = 5
Nrange = np.linspace(10, 20, Ns).astype(int)

filenames = ["data/data{}.out".format(i) for i in Nrange]

def file_exists(filename):
    return bool(os.path.isfile(filename))

plt.figure()
for i, (N, filename) in enumerate(zip(Nrange, filenames)):
    # Simulate
    if not file_exists(filename):
        os.system('./sim config_bc.in "N={}" "filename={}" "temperature={}"'.format(N, filename, T))

    data = np.loadtxt(filename)
    x = data[:, 0]
    E = data[:, 1] / N ** 3
    plt.plot(x, E, label="N={}".format(N))

plt.legend()
plt.show()


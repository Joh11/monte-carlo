"""A script to plot the HT scan"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

scandir = "data/scan/"

files = os.listdir(scandir)


Hs = []
Ts = []
Mzs = []

for fname in files:
    s = fname[5:-3]
    H, T = s.split('_')
    H = float(H)
    T = float(T)
    Hs.append(H)
    Ts.append(T)
    
    data = np.loadtxt(scandir + fname)
    Mz = np.mean(data[:, -1])

    Mzs.append(Mz)

Hs = np.array(Hs)
Ts = np.array(Ts)
Mzs = np.array(Mzs)
    
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(Hs, Ts, Mzs, color='green')
ax.set_xlabel('H')
ax.set_ylabel('T')
ax.set_zlabel('M_z per site')

plt.show()

import numpy as np
import os
import matplotlib.pyplot as plt

prefix = "sim_"
Ns = np.array([10, 15, 20, 30])
workdir = os.path.abspath("monte-carlo/") + "/"

datas = []
for N in Ns:
    data = np.loadtxt(workdir + prefix + "{}/data.out".format(N))
    datas.append(data[:, 0:3])


plt.figure()
plt.xlabel("steps")
plt.ylabel("E")

for N, data in zip(Ns, datas):
    plt.plot(data[:, 0], data[:, 1], label="N={}".format(N))

plt.legend()
plt.savefig("E.png")

plt.figure()
plt.xlabel("steps")
plt.ylabel("Mx")

for N, data in zip(Ns, datas):
    plt.plot(data[:, 0], data[:, 2], label="N={}".format(N))

plt.legend()
plt.savefig("Mx.png")

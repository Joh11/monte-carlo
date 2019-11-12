import sys
import numpy as np
import matplotlib.pyplot as plt

filename = "data/data.out"
Nlast = 10

if len(sys.argv) >= 2:
    filename = sys.argv[1]

if len(sys.argv) >= 3:
    Nlast = sys.argv[1]

data = np.loadtxt(filename)

it = data[:, 0]
E = data[:, 5]
M = data[:, 6:9]

Mz = M[:, 2]

print("Using the last {} samples : ".format(Nlast))
print("Mean energy per site : {} +- {}".format(np.mean(E[-Nlast:]), np.std(E[-Nlast:])))
print("Mean magnetization per site : {}".format(np.mean(M[-Nlast:, :], axis=0)))

# Plot energy against iteration
plt.subplot(2, 1, 1)
plt.plot(it, E)
plt.xlabel("Iteration []")
plt.ylabel("Energy per site []")

plt.subplot(2, 1, 2)
plt.plot(it, Mz)
plt.xlabel("Iteration []")
plt.ylabel("Magnetization in Z per site []")

plt.show()

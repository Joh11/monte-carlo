import sys
import numpy as np
import matplotlib.pyplot as plt

filename = "data/data.out"

if len(sys.argv) >= 2:
    filename = sys.argv[1]

data = np.loadtxt(filename)

it = data[:, 0]
E = data[:, 1]
M = data[:, 2:5]

Mz = M[:, 2]

# Plot energy against iteration
plt.subplot(2, 1, 1)
plt.plot(it, E)
plt.xlabel("Iteration []")
plt.ylabel("Energy [?]")

plt.subplot(2, 1, 2)
plt.plot(it, Mz)
plt.xlabel("Iteration []")
plt.ylabel("Magnetization in Z[?]")

plt.show()

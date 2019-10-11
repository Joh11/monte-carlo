import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("data/data.out")

it = data[:, 0]
E = data[:, 1]
M = data[:, 2:5]

Mnorm = np.linalg.norm(M, axis=1)

# Plot energy against iteration
plt.subplot(2, 1, 1)
plt.plot(it, E)
plt.xlabel("Iteration []")
plt.ylabel("Energy [?]")

plt.subplot(2, 1, 2)
plt.plot(it, Mnorm)
plt.xlabel("Iteration []")
plt.ylabel("Magnetization [?]")

plt.show()

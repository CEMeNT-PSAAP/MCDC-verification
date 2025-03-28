import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py
import sys

# Reference solution
data = np.load("reference.npz")
x_edge = data["x"]
dx_ref = np.diff(x_edge)
x_ref = (x_edge[:-1] + x_edge[1:]) / 2
phi_edge = data["phi"]
phi_ref = (data["phi"][:-1] + data["phi"][1:]) / 2
phi_ref /= phi_ref[0]

# Get results
output = sys.argv[1]
with h5py.File(output, "r") as f:
    x = f["tallies/mesh_tally_0/grid/x"][:]
    dx = np.diff(x)
    x_mid = 0.5 * (x[:-1] + x[1:])

    phi = f["tallies/mesh_tally_0/flux/mean"][:] / dx
    phi_sd = f["tallies/mesh_tally_0/flux/sdev"][:] / dx

    # Normalize
    phi /= phi[0] 
    phi_sd /= phi[0]

print(phi_ref)
print(phi)

# Flux - spatial average
plt.plot(x_mid, phi, "-b", label="MC")
plt.fill_between(x_mid, phi - phi_sd, phi + phi_sd, alpha=0.2, color="b")
plt.plot(x_ref, phi_ref, "-r", label="Reference")
plt.xlabel(r"$x$, cm")
plt.ylabel("Flux")
plt.grid()
plt.legend()
plt.title(r"$\bar{\phi}_i$")
plt.savefig("scalar_flux.png", dpi=300)
plt.show()
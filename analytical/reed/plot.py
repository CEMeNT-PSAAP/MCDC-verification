import matplotlib.pyplot as plt
import h5py
import sys

from reference import reference

# Reference solution
output = sys.argv[1]

# Load results
with h5py.File(output, "r") as f:
    x = f["tallies/mesh_tally_0/grid/x"][:]
    dx = x[1:] - x[:-1]
    x_mid = 0.5 * (x[:-1] + x[1:])
    I = len(x) - 1

    phi = f["tallies/mesh_tally_0/flux/mean"][:]
    phi_sd = f["tallies/mesh_tally_0/flux/sdev"][:]

# Normalize
phi, phi_sd = phi / dx, phi_sd / dx
x_ref, phi_ref = reference()

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

from reference import reference
import numpy as np
import h5py
import sys

sys.path.append("../")
import tool

# Cases run
N_min = int(sys.argv[1])
N_max = int(sys.argv[2])
N = int(sys.argv[3])
N_particle_list = np.logspace(N_min, N_max, N)

# Reference solution
data = np.load("reference.npz")
phi_edge = data["phi"]
phi_ref = (data["phi"][:-1] + data["phi"][1:]) / 2
phi_ref /= phi_ref[0]
k_ref = data["k"]

# Error containers
error_k = np.zeros(len(N_particle_list))
error_max_k = np.zeros(len(N_particle_list))
error_f = np.zeros(len(N_particle_list))
error_max_f = np.zeros(len(N_particle_list))

# Calculate error
for i, N_particle in enumerate(N_particle_list):
    # Get results
    with h5py.File("output_%i.h5" % (int(N_particle)), "r") as f:
        x = f["tallies/mesh_tally_0/grid/x"][:]
        dx = np.diff(x)
        x_mid = 0.5 * (x[:-1] + x[1:])
        phi = f["tallies/mesh_tally_0/flux/mean"][:]
        k = np.array(f["k_mean"])
        
    # Normalize
    phi /= dx
    phi /=  phi[0]
  
    # Get error
    error_f[i] = tool.error(phi, phi_ref)
    error_max_f[i] = tool.error_max(phi, phi_ref)
    error_k[i] = tool.error(k, k_ref)
    error_max_k[i] = tool.error_max(k, k_ref)

print(error_f)
print(error_max_f)
print(error_k)
print(error_max_k)
print(k_ref)
print(k)

print(phi_ref)
print(phi)

# Plot
tool.plot_convergence("kornreich_flux", N_particle_list, error_f, error_max_f)
tool.plot_convergence_k("kornreich_k_eigenvalue", N_particle_list, error_k)
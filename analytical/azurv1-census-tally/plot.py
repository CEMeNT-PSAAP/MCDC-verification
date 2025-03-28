import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py


# Reference solution
data = np.load("reference.npz")
phi_ref = data["phi"]

# The grids
x = np.linspace(-20.5, 20.5, 202)
t = np.linspace(0.0, 20.0, 21)
dx = x[1:] - x[:-1]
x_mid = 0.5 * (x[:-1] + x[1:])
dt = t[1:] - t[:-1]
J = len(dx)
K = len(dt)

# Get the solution
phi = np.zeros((K, J))
N_census = 4
N_batch = 10
for i_census in range(N_census):
    for i_batch in range(N_batch):
        with h5py.File("output-batch_%i-census_%i.h5" % (i_batch, i_census), "r") as f:
            phi[5 * i_census : 5 * i_census + 5, :] += f[
                "tallies/mesh_tally_0/flux/score"
            ][:]
    phi[5 * i_census : 5 * i_census + 5] /= N_batch

# Normalize
for k in range(K):
    phi[k] /= dx * dt[k]

# Flux - average
fig = plt.figure()
ax = plt.axes(
    # xlim=(-21.889999999999997, 21.89), ylim=(-0.042992644459595206, 0.9028455336514992)
    xlim=(-21.889999999999997, 21.89),
    ylim=(1e-7, 0.9028455336514992),
)
ax.grid()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"Flux")
ax.set_title(r"$\bar{\phi}_{k,j}$")
(line1,) = ax.plot([], [], "-b", label="MC")
(line2,) = ax.plot([], [], "--r", label="Ref.")
# fb = ax.fill_between([], [], [], [], alpha=0.2, color="b")
text = ax.text(0.02, 0.9, "", transform=ax.transAxes)
ax.legend()
ax.set_yscale("log")


def animate(k):
    # global fb
    # fb.remove()
    line1.set_data(x_mid, phi[k, :])
    # fb = ax.fill_between(
    #    x_mid, phi[k, :] - phi_sd[k, :], phi[k, :] + phi_sd[k, :], alpha=0.2, color="b"
    # )
    line2.set_data(x_mid, phi_ref[k, :])
    text.set_text(r"$t \in [%.1f,%.1f]$ s" % (t[k], t[k + 1]))
    return line1, line2, text


simulation = animation.FuncAnimation(fig, animate, frames=K)
writervideo = animation.FFMpegWriter(fps=6)
plt.show()

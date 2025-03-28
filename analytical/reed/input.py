import mcdc
import numpy as np

# =============================================================================
# Set model
# =============================================================================
# Four slab layers with different materials
# Based on William H. Reed, NSE (1971), 46:2, 309-314, DOI: 10.13182/NSE46-309

#Set materials
m1 = mcdc.material(capture=np.array([50.0]), scatter=np.array([[0.0]]))
m2 = mcdc.material(capture=np.array([5.0]), scatter=np.array([[0.0]]))
m3 = mcdc.material(capture=np.array([0.0]), scatter=np.array([[0.0]]))
m4 = mcdc.material(capture=np.array([0.1]), scatter=np.array([[0.9]]))

#Set surfaces
s1 = mcdc.surface("plane-x", x=0.0, bc='reflective')
s2 = mcdc.surface("plane-x", x=2.0, bc='interface')
s3 = mcdc.surface("plane-x", x=3.0, bc='interface')
s4 = mcdc.surface("plane-x", x=5.0, bc='interface')
s5 = mcdc.surface("plane-x", x=8.0, bc='vacuum')

#Set cells
c1 = mcdc.cell(+s1 & -s2, m1)
c2 = mcdc.cell(+s2 & -s3, m2)
c3 = mcdc.cell(+s3 & -s4, m3)
c4 = mcdc.cell(+s4 & -s5, m4)

# =============================================================================
# Set source
# =============================================================================

mcdc.source(
    x=[0.0, 2.0],
    isotropic=True,
    prob=50.0
)

mcdc.source(
    x=[5.0, 6.0],
    isotropic=True,
    prob=0.5
)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

#Tally
mcdc.tally.mesh_tally(
    scores=["flux"],
    x=np.linspace(0.0, 8.0, 81),
)

#Setting
mcdc.setting(N_particle=10000)

#Run
mcdc.run()

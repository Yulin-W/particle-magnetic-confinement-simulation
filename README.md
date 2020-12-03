# Simulation of Confinement Behaviour of Charged Particles in Magnetic Fields, particularly tokamaks

# Introduction
Tokamaks are devices designed to confine plasma with toroidal magnetic fields induced by electromagnets to facilitate nuclear fusion. The key behind such confinement is that charges tend to gyrate (spiral) along magnetic field lines. In practice, charge clustering also lead to electric fields, which must be accounted for when analyzing magnetic field confinement.

In this simulation, we simulate the behaviours of charge particules in various field configurations (both magnetic and electric), and through this investigate conditions maximising particle confinement time in a tokamak.

# Report summary
Tokamak confinement time was found to be maximised with weak electric fields (low ion density), low particle speeds (low temperature) and large coil number (strong magnetic field). Quantitatively however, each variable’s effects on confinement time depend on the specific set of variable values; in certain cases, some variables will dominate over others regarding influence over confinement time.

# Visualizations of produced data (demonstrating how charges behave in various fields)
![]()

# Other
- data_viewer.py opens a GUI for easier visualization of the generated data
- the 3 data_generator.py scripts were used to generate the data of the paths of particles (stored in .pkl format)
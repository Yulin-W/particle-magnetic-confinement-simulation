import numpy as np
import em
import visualisation
from simulation import Simulation
import utility

# All units are in standard SI units

# Setting up test cases
uniform_B = {
    "field" : em.Uniform_B_Field(B_vector=np.array([0,20.867*10**(-8),0], utility.dtype)),
    "timestep" : 0.001,
    "simulation_time" : 3,
    "electron_positions" : None,
    "electron_velocities" : None,
    "deuterium_positions" : (np.array([0,0,0.1], utility.dtype), ),
    "deuterium_velocities" : (np.array([1,1,0], utility.dtype), ),
}

uniform_B_elec = {
    "field" : em.Uniform_B_Field(B_vector=np.array([0,20.867*10**(-8),0], utility.dtype)),
    "timestep" : 0.0000005, # time step is much smaller than for deuterium as testing showed that electron simulations will produce rapidly accumulating approximation errors with larger time steps
    "simulation_time" : 0.001,
    "electron_positions" : (np.array([0,0,-2.5*10**(-5)], utility.dtype), ),
    "electron_velocities" : (np.array([1,1,0], utility.dtype), ),
    "deuterium_positions" : None,
    "deuterium_velocities" : None,
}

uniform_EB = {
    "field" : em.EB_Field(B_vector=np.array([0,20.867*10**(-8),0], utility.dtype), E_vector=np.array([0,0,20.867*10**(-8)], utility.dtype)),
    "timestep" : 0.01,
    "simulation_time" : 3.,
    "electron_positions" : None,
    "electron_velocities" : None,
    "deuterium_positions" : (utility.zero_vec.copy(), ),
    "deuterium_velocities" : (np.array([1,1,0], utility.dtype), ),
}

uniform_EB_elec = {
    "field" : em.EB_Field(B_vector=np.array([0,20.867*10**(-8),0], utility.dtype), E_vector=np.array([0,0,20.867*10**(-8)], utility.dtype)),
    "timestep" : 0.000001,
    "simulation_time" : 0.1,
    "electron_positions" : (utility.zero_vec.copy(),),
    "electron_velocities" : (np.array([1,1,0], utility.dtype),),
    "deuterium_positions" : None,
    "deuterium_velocities" : None,
}

uniform_GB = {
    "field" : em.GB_Field(B_vector=np.array([0,20.867*10**(-8),0], utility.dtype), G_vector=np.array([0,0,-9.8], utility.dtype)),
    "timestep" : 0.001,
    "simulation_time" : 3.,
    "electron_positions" : None,
    "electron_velocities" : None,
    "deuterium_positions" : (utility.zero_vec.copy(), ),
    "deuterium_velocities" : (np.array([1,1,0], utility.dtype), ),
}

uniform_GB_elec = {
    "field" : em.GB_Field(B_vector=np.array([0,20.867*10**(-8),0], utility.dtype), G_vector=np.array([0,0,-9.8], utility.dtype)),
    "timestep" : 0.000001,
    "simulation_time" : 0.001,
    "electron_positions" : (utility.zero_vec.copy(), ),
    "electron_velocities" : (np.array([1,1,0], utility.dtype), ),
    "deuterium_positions" : None,
    "deuterium_velocities" : None,
}

toroidal_B = {
    "field" : em.Toroidal_B_Field(utility.dtype(100), utility.dtype(0.03), utility.dtype(0.5), utility.dtype(1.5)),
    "timestep" : 0.005,
    "simulation_time" : 5,
    "electron_positions" : None,
    "electron_velocities" : None,
    "deuterium_positions" : (np.array([1,0,-0.4], utility.dtype),),
    "deuterium_velocities" : (np.array([2,2,0], utility.dtype),),
}

toroidal_B_elec = {
    "field" : em.Toroidal_B_Field(utility.dtype(100), utility.dtype(0.00005), utility.dtype(0.5), utility.dtype(1.5)),
    "timestep" : 0.001,
    "simulation_time" : 2,
    "electron_positions" : (np.array([1,0,0.4], utility.dtype), ),
    "electron_velocities" : (np.array([12,2,0], utility.dtype), ),
    "deuterium_positions" : None,
    "deuterium_velocities" : None,
}

tokamak = {
    "field" : em.Tokamak_Field(utility.dtype(200), utility.dtype(0.05), utility.dtype(0.5), utility.dtype(1.5), np.array([0,0,-20.867*10**(-8)], utility.dtype), np.array([0,0,-9.8], utility.dtype)),
    "timestep" : 0.001,
    "simulation_time" : 4,
    "electron_positions" : None,
    "electron_velocities" : None,
    "deuterium_positions" : (np.array([1,0,-0.4], utility.dtype),),
    "deuterium_velocities" : (np.array([4,4,0], utility.dtype),),
}

tokamak_elec = {
    "field" : em.Tokamak_Field(utility.dtype(100), utility.dtype(0.005), utility.dtype(0.5), utility.dtype(1.5), np.array([0,0,-80.867*10**(-7)], utility.dtype), np.array([0,0,-9.8], utility.dtype)),
    "timestep" : 0.00001,
    "simulation_time" : 0.1,
    "electron_positions" : (np.array([1,0,0.4], utility.dtype), ),
    "electron_velocities" : (np.array([2000,1000,0], utility.dtype), ),
    "deuterium_positions" : None,
    "deuterium_velocities" : None,
}

# Individual simulation test cases 
#   - To run specific simulation, uncomment corresponding load_settings line and run sim.generate_data())
#   - To output data to specific file (stored in Data folder), run sim.output_data(filename to save to) after running simulation
#   - To plot, animate simulation, run sim.visualise with appropriate visualisation settings after running simulation to generate data

# Initialises simulation object
# sim = Simulation()

# Code for loading simulation test cases
# sim.load_settings(uniform_B)
# sim.load_settings(uniform_B_elec)
# sim.load_settings(uniform_EB)
# sim.load_settings(uniform_EB_elec)
# sim.load_settings(uniform_GB)
# sim.load_settings(uniform_GB_elec)
# sim.load_settings(toroidal_B)
# sim.load_settings(toroidal_B_elec)
# sim.load_settings(tokamak)
# sim.load_settings(tokamak_elec)

# Data generation
# sim.generate_data()

# Visualisation settings for checking data: note visualisations are generally pannable and resizable by mouse; however doing so may by laggy especially when vectors are plotted alongside
# Note: plotted vectors are all normalized and, if specific vector length given, scaled to that length; i.e. relative vector magnitudes are not displayed
# sim.visualise("plot", to_proportion=True)
# sim.visualise("anime", 5, to_proportion=True)
# sim.visualise("plot", to_proportion=True, plot_vectors=True, vector_plot_length=0.3)
# sim.visualise("plot", to_proportion=True, plot_vectors=True, vector_plot_length=0.00005, vector_num=5) # for uniform_EB_elec case
# sim.visualise("plot", custom_limits=((2,-2), (2,-2), (2,-2))) # for toroidal field and tokamak field
# sim.visualise("plot", plot_vectors=True, vector_plot_length=0.3, vector_num=5, custom_limits=((2,-2), (2,-2), (2,-2))) # for toroidal field and tokamak field
# sim.visualise("plot", custom_limits=((6,-6), (6,-6), (6,-6))) # for tokamak field with inner radius 2, outer radius 6

# Outputting data to "General Data" folder under specified name in the second argument in .pkl file format
# sim.output_data("General Data", "uniform_EB_elec")

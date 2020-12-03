import numpy as np
import em
import visualisation
from simulation import Simulation
import utility
import random
import os
import json

# All units are in standard SI units

# Function for generating tokamak simulation settings
def generate_tokamak_settings(temperature, coil_num, ion_density, simulation_time, timestep):
    """Returns settings dictionary for tokamak based on 3 input variables; temperature, number of coils, ion density
    Args:
        temperature: temperature value for particles to simulate in K
        coil_num: number of rings of coils around the toroid (assumed current through them is 1 A)
        ion_densty: number of deuterium ions per m^3 inside the tokamak (electron density assumed to be the same)
        simulation_time: length of time to be simulated in s
        timestep: time step size for RK4 differential solver in s

    Sets 5 electrons and 5 deuterium ions
    Electron and deuterium velocities are randomly generated 3-tuple direction vectors consisting of integers from 0-9 scaled for average speed corresponding to given temperature
    Electron and deuterium positions are randomly generated 3-tuples of floats within the torus lying on the cylindric surface of radius 4, height 2 symmetric about x-y plane and axis of rotation x=y=0; 
    this ensures initial starting locations are well away magnetic field boundaries (to avoid ambiguity with confinement escape detection)
    """
    # Initialises particle velocity and position parameters
    avg_velocity_deut = utility.dtype(np.sqrt(8*utility.gas_constant*temperature / (np.pi*utility.deuterium_molar_mass)))
    avg_velocity_elec = utility.dtype(np.sqrt(8*utility.gas_constant*temperature / (np.pi*utility.electron_molar_mass)))
    deut_directions = [np.array((random.randrange(10), random.randrange(10), random.randrange(10)), utility.dtype) for _ in range(5)]
    elec_directions = [np.array((random.randrange(10), random.randrange(10), random.randrange(10)), utility.dtype) for _ in range(5)]
    
    deut_x = [random.uniform(-4,4) for _ in range(5)]
    elec_x = [random.uniform(-4,4) for _ in range(5)]

    # Computes electric field within toroid based on an approximating assumption that 10% of ions/electrons form parallel plates of charge on the top and bottom of the torus (thus accounting for charge separation due to drift velocities)
    E_strength = ion_density * 4 * 0.1 * utility.elementary_charge / utility.permittivity_of_free_space

    return {
        "field" : em.Tokamak_Field(utility.dtype(coil_num), utility.dtype(1), utility.dtype(2), utility.dtype(6), np.array([0,0,-E_strength], utility.dtype), np.array([0,0,-9.8], utility.dtype)),
        "timestep" : timestep,
        "simulation_time" : simulation_time,
        "electron_positions" : [np.array(( x, random.choice([np.sqrt(16-x**2), -np.sqrt(16-x**2)]),  random.uniform(-1,1) ), utility.dtype) for x in elec_x], # in m
        "electron_velocities" : [avg_velocity_elec * direction for direction in elec_directions], # in m/s
        "deuterium_positions" : [np.array(( x, random.choice([np.sqrt(16-x**2), -np.sqrt(16-x**2)]), random.uniform(-1,1) ), utility.dtype) for x in deut_x], # in m
        "deuterium_velocities" : [avg_velocity_deut * direction for direction in deut_directions], # in m/s
    }

# Function for generating data samples for tokamak simulation varying each of the 3 variables individually symmetrically around set initial value with respective step sizes linearly; 21 data points are taken for each variable
def generate_data_samples_linear(settings):
    # Initialise simulation object
    sim = Simulation()

    # Initialise the range of variable values to test
    variable_vals = {
        "temperature" : [settings["temperature"] + i * settings["temperature_step"] for i in range(-10,11)],
        "coil_num" : [settings["coil_num"] + i * settings["coil_num_step"] for i in range(-10,11)],
        "ion_density" : [settings["ion_density"] + i * settings["ion_density_step"] for i in range(-10,11)],
    }

    # Setup file directory
    folder_path = os.path.join(os.getcwd(), "ITER Tokamak Data", settings["folder"])
    if not os.path.isdir(folder_path): # creates folder if doesn't already exist
        os.mkdir(folder_path)

    # Save simulation settings to a json file in directory
    with open(os.path.join(folder_path, "settings.json"), "w") as f:
        json.dump(settings, f)

    # Initialise base settings
    base_settings = dict({item for item in settings.items() if item[0] in ("temperature", "coil_num", "ion_density", "simulation_time", "timestep")})

    # Loop over the settings with variables changed accordingly and output data
    for variable, values in variable_vals.items():
        for value in values:
            current_settings = base_settings.copy()
            current_settings[variable] = value
            sim.load_settings(generate_tokamak_settings(**current_settings))
            sim.generate_data()
            sim.output_data(folder_path, variable+"_"+str(value))

# Settings for the two scenario sets tested
data_sample_settings_ITER = {
    "temperature" : 10**8,
    "temperature_step" : 9*10**6, 
    "coil_num" : 10**8,
    "coil_num_step" : 9*10**6,
    "ion_density" : 10**(19),
    "ion_density_step" : 9*10**(17),
    "simulation_time" : 10**(-8),
    "timestep" : 2*10**(-12),
    "folder" : "iter_simulation", 
}

data_sample_settings_ITER_weak_E = {
    "temperature" : 10**8,
    "temperature_step" : 9*10**6, 
    "coil_num" : 10**8,
    "coil_num_step" : 9*10**6,
    "ion_density" : 10**(15),
    "ion_density_step" : 9*10**(13),
    "simulation_time" : 10**(-8),
    "timestep" : 10**(-12),
    "folder" : "iter_simulation_weak_E", 
}

# Sample data generation for ITER tokamak setting
# generate_data_samples_linear(data_sample_settings_ITER)

# Sample data generation for ITER weak_E tokamak setting
# generate_data_samples_linear(data_sample_settings_ITER_weak_E)

# Some tokamak test cases
# To run, uncomment sim = Simulation(), sim.load_settings code block containing desired simulation settings, sim.generate_data() to generate simulation data, and print confinement time/sim.visualise/sim.output_data for corresponding additional actions if necessary

# sim = Simulation()

# Case Simulating ITER Specifications
"""
sim.load_settings(generate_tokamak_settings(**{
    "temperature" : 10**8,
    "coil_num" : 10**8,
    "ion_density" : 10**(19),
    "simulation_time" : 10**(-8),
    "timestep" : 2*10**(-12),
}))
"""

# Case Simulating ITER Specifications but with weaker electric field
"""
sim.load_settings(generate_tokamak_settings(**{
    "temperature" : 10**8,
    "coil_num" : 10**8,
    "ion_density" : 10**(15),
    "simulation_time" : 10**(-8),
    "timestep" : 10**(-12),
}))
"""

# Case simulating ITER specifications but much much weaker electric field
"""
sim.load_settings(generate_tokamak_settings(**{
    "temperature" : 10**8,
    "coil_num" : 10**8,
    "ion_density" : 10**(1),
    "simulation_time" : 10**(-8),
    "timestep" : 2*10**(-12),
}))
"""

# sim.generate_data()
# print(sim.data["confinement_times"])

# sim.visualise("plot", custom_limits=((6,-6), (6,-6), (6,-6)))

# Data Output
# sim.output_data("ITER Tokamak Test Case Data", "ITER_very weak_E")

import numpy as np
import em
import visualisation
from simulation import Simulation
import utility
import random
import os
import json

# All units are in standard SI units

def generate_small_value_tokamak_settings(coil_num, E_field, speed, simulation_time, timestep):
    """Returns settings dictionaries for tokamak based on 3 input variables; temperature, number of coils, ion density
    Args:
        coil_num: number of rings of coils around the toroid (assumed current through them is 0.05 A)
        E_field: electric field strength in N/C
        speed: speed scalar of particles in m/s
        simulation_time: length of time to be simulated in s
        timestep: time step size for RK4 differential solver in s

    Sets 10 deuterium ions
    Deuterium velocities are randomly generated 3-tuple direction vectors consisting of integers from 0-9 scaled for average speed
    Deuterium positions are randomly generated 3-tuples of floats within the torus lying on the cylindric surface of radius 4, height 2 symmetric about x-y plane and axis of rotation x=y=0; 
    this ensures initial starting locations are well away magnetic field boundaries (to avoid ambiguity with confinement escape detection)
    """
    # Initialises particle velocity and position parameters
    deut_directions = [np.array((random.randrange(10), random.randrange(10), random.randrange(10)), utility.dtype) for _ in range(10)]
    
    deut_x = [random.uniform(-4,4) for _ in range(10)]

    return {
        "field" : em.Tokamak_Field(utility.dtype(coil_num), utility.dtype(0.05), utility.dtype(2), utility.dtype(6), np.array([0,0,-E_field], utility.dtype), np.array([0,0,-9.8], utility.dtype)),
        "timestep" : timestep,
        "simulation_time" : simulation_time,
        "electron_positions" : None,
        "electron_velocities" : None,
        "deuterium_positions" : [np.array(( x, random.choice([np.sqrt(16-x**2), -np.sqrt(16-x**2)]), random.uniform(-1,1) ), utility.dtype) for x in deut_x], # in m
        "deuterium_velocities" : [speed * direction for direction in deut_directions], # in m/s
    }

def generate_small_value_tokamak_data_linear(settings):
    # Initialise simulation object
    sim = Simulation()

    # Initialise the range of variable values to test
    variable_vals = {
        "coil_num" : [settings["coil_num"] + i * settings["coil_num_step"] for i in range(-10,11)],
        "E_field" : [settings["E_field"] + i * settings["E_field_step"] for i in range(-10,11)],
        "speed" : [settings["speed"] + i * settings["speed_step"] for i in range(-10,11)],
    }

    # Setup file directory
    folder_path = os.path.join(os.getcwd(), "Small Value Tokamak Data", settings["folder"])
    if not os.path.isdir(folder_path): # creates folder if doesn't already exist
        os.mkdir(folder_path)

    # Save simulation settings to a json file in directory
    with open(os.path.join(folder_path, "settings.json"), "w") as f:
        json.dump(settings, f)

    # Initialise base settings
    base_settings = dict({item for item in settings.items() if item[0] in ("coil_num", "E_field", "speed", "simulation_time", "timestep")})
    
    # Loop over the settings with variables changed accordingly and output data
    for variable, values in variable_vals.items():
        for value in values:
            current_settings = base_settings.copy()
            current_settings[variable] = value
            sim.load_settings(generate_small_value_tokamak_settings(**current_settings))
            sim.generate_data()
            sim.output_data(folder_path, variable+"_"+str(value))

# Settings for the 2 scenario sets tested
data_settings = {
    "coil_num" : 200,
    "coil_num_step" : 15 ,
    "E_field" : 10**(-7),
    "E_field_step" : 9*10**(-9),
    "speed" : 3,
    "speed_step" : 0.2,
    "simulation_time" : 10,
    "timestep" : 0.001,
    "folder" : "data_1", 
}

data_settings_stronger_magnetic_field = {
    "coil_num" : 2000,
    "coil_num_step" : 150 ,
    "E_field" : 10**(-7),
    "E_field_step" : 9*10**(-9),
    "speed" : 3,
    "speed_step" : 0.2,
    "simulation_time" : 10,
    "timestep" : 0.001,
    "folder" : "data_stronger_magnetic_field",
}

# Command for generating and outputting data samples corresponding to settings in the argument of below
generate_small_value_tokamak_data_linear(data_settings)
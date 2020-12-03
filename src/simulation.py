import numpy as np
import em
import visualisation

# Modules for saving
import pickle
import json
import os

class Simulation:
    def __init__(self):
        self.data = None
    
    def load_settings(self, settings):
        """Loads simulation settings (a dictionary)
        """
        self.settings = settings

    def generate_data(self):
        """Generates simulation data
        """
        self.data = {}
        self.data["settings"] = self.settings
        self.data["visualisation_settings"] = {}

        # Deals with cases where there are only deuterium ions, only electrons or there are both
        if self.settings["electron_positions"] == None:
            self.data["visualisation_settings"].update({
                "path_labels" : ("Deuterium",),
                "path_colors" : ("b",),
                "sets_color_ind" : len(self.settings["deuterium_positions"]) * [0]
            })
            deuterium_ions = [em.Deuterium_Ion(position=position, velocity=velocity, field=self.settings["field"]) for (position, velocity) in zip(self.settings["deuterium_positions"], self.settings["deuterium_velocities"])]
            particles = deuterium_ions
        elif self.settings["deuterium_positions"] == None:
            self.data["visualisation_settings"].update({
                "path_labels" : ("Electron",),
                "path_colors" : ("r",),
                "sets_color_ind" : len(self.settings["electron_positions"]) * [0]
            })
            electrons = [em.Electron(position=position, velocity=velocity, field=self.settings["field"]) for (position, velocity) in zip(self.settings["electron_positions"], self.settings["electron_velocities"])]
            particles = electrons
        else:
            self.data["visualisation_settings"].update({
                "path_labels" : ("Deuterium", "Electron"),
                "path_colors" : ("b", "r"),
                "sets_color_ind" : len(self.settings["deuterium_positions"]) * [0] + len(self.settings["electron_positions"]) * [1]
            })
            deuterium_ions = [em.Deuterium_Ion(position=position, velocity=velocity, field=self.settings["field"]) for (position, velocity) in zip(self.settings["deuterium_positions"], self.settings["deuterium_velocities"])]
            electrons = [em.Electron(position=position, velocity=velocity, field=self.settings["field"]) for (position, velocity) in zip(self.settings["electron_positions"], self.settings["electron_velocities"])]
            particles = deuterium_ions + electrons

        # Initialises data holders and simulation time recorder
        data = [[[], [], []] for _ in range(len(self.data["visualisation_settings"]["sets_color_ind"]))]
        time = 0
        confinement_times = [False] * len(particles)
        # Initialses dictionary used for reporting data generation progress
        generation_progress_report = {proportion*self.settings["simulation_time"]:[percent, False] for (proportion, percent) in [(0.05*i, str(i*5)+"%") for i in range(20)]} # key is time passed corresponding to the proportional completion, percent is a string with the percentage, the False value is to indicate the percentage hasn't been passed yet
        # Loops over time steps determined by specified simulation time and timestep settings
        for _ in range(round(self.settings["simulation_time"] / self.settings["timestep"])):
            time += self.settings["timestep"] # increments time recorder
            for ind, particle in enumerate(particles): # loops over particles
                for index, axis in enumerate(data[ind]):
                    axis.append(particle.position[index]) # record new particle position
                escaped_confinement = particle.update(self.settings["timestep"])
                if escaped_confinement: # recording particle confinement escape
                    confinement_times[ind] = time
            # Reporting generation progress
            for progress in generation_progress_report.keys(): # loops over the milestone times corresponding to completion progress to check for whether a new milestone has been passed
                if time >= progress and generation_progress_report[progress][1] == False: # if a new milestone has been passed
                    generation_progress_report[progress][1] = True # set the milestone's passed status to True
                    print(generation_progress_report[progress][0]) # print corresponding progress completion
                    break # break out of the milestone time checking loop
        else: # After data generation complete
            print("Done") 
                
        self.data["data"] = data # assigns the generated data to self.data dictionary
        self.data["confinement_times"] = confinement_times # assign confinement times found to self.data dictionary

    def visualise(self, plot_or_anime, anime_time=10, fps=20, to_proportion=False, custom_limits=None, plot_vectors=False, vector_plot_length=0, vector_num=5):
        """Generates data visualisation according to inputted visualisation arguments
        """
        if self.data:
            # Initialises a Visualiser class instance with corresponding visualisation settings
            visualiser = visualisation.Visualiser(self.data["visualisation_settings"], self.data["data"], self.data["settings"]["field"].field_methods, to_proportion, custom_limits)
            if plot_or_anime == "plot":
                visualiser.plot_3d(plot_vectors, vector_plot_length, vector_num)
            elif plot_or_anime == "anime":
                visualiser.animate_3d(anime_time, fps, plot_vectors, vector_plot_length, vector_num)

    def load_data(self, folder=None, filename=None, absolute_path=None):
        """Loadss data from .pkl files at location according to specified argument values into self.data attribute of class instance
        """
        if absolute_path:
            file_path = absolute_path
        else:
            output_folder = os.path.join(os.getcwd(), folder)
            file_path = os.path.join(output_folder, filename+".pkl")
        with open(file_path, "rb") as f:
            self.data = pickle.load(f)

    def output_data(self, folder=None, filename=None, absolute_path=None):
        """Outputs data file in .pkl format to a file at location according to specified argument values
        """
        if self.data:
            if absolute_path:
                file_path = absolute_path
            else:
                output_folder = os.path.join(os.getcwd(), folder)
                file_path = os.path.join(output_folder, filename+".pkl")
            with open(file_path, "wb") as f:
                pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
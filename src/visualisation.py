import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
import utility

class Visualiser:
    """
    Handles plotting and animation visualisations
    """
    def __init__(self, visualisation_settings, point_sets, field_methods, to_proportion=False, custom_limits=None):
        self.visualisation_settings = visualisation_settings # contains settings such as colour of paths, path labels to appear in legend, etc.
        self.point_sets = point_sets
        self.sets_num = len(self.point_sets)
        self.points_num = len(self.point_sets[0][0])
        self.labels_num = len(self.visualisation_settings["path_labels"])
        self.field_methods = field_methods
        self.field_colors = ["grey", "turquoise", "orange"] # set of colours for different vector fields to use
        # Sets visualisation axes limits
        if custom_limits:
            self.x_min = custom_limits[0][0]
            self.x_max = custom_limits[0][1]
            self.y_min = custom_limits[1][0]
            self.y_max = custom_limits[1][1]
            self.z_min = custom_limits[2][0]
            self.z_max = custom_limits[2][1]
        else:
            self.x_max = max([max(sets[0]) for sets in self.point_sets])
            self.y_max = max([max(sets[1]) for sets in self.point_sets])
            self.z_max = max([max(sets[2]) for sets in self.point_sets])
            self.x_min = min([min(sets[0]) for sets in self.point_sets])
            self.y_min = min([min(sets[1]) for sets in self.point_sets])
            self.z_min = min([min(sets[2]) for sets in self.point_sets])

            if to_proportion:
                min_limits = min((self.x_min, self.y_min, self.z_min)) 
                max_limits = max((self.x_max, self.y_max, self.z_max))
                self.x_min = self.y_min = self.z_min = min_limits
                self.x_max = self.y_max = self.z_max = max_limits

    
    def plot_3d(self, plot_vectors=False, vector_plot_length=0, vector_num=5):
        """Uses self.point_sets to plot and diplays a figure with all of the curves/paths

        Arguments:
            plot_vectors: boolean value indicating whether to plot vectors or not
            vector_plot_length: length of plotted vectors (will all have the same lengths) in the scale of the plot
            vector_num: number of vectors to plot per axis direction (e.g. 5 means will plot 5*5*5 = 125 vectors per vector field)
        """
        # Basic setup
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(self.y_min, self.y_max)
        ax.set_zlim(self.z_min, self.z_max)

        # Setup path plots
        for ind, sets in enumerate(self.point_sets):
            ax.plot3D(sets[0], sets[1], sets[2], self.visualisation_settings["path_colors"][self.visualisation_settings["sets_color_ind"][ind]]+",")
        # Setup path plot legends via empty plots (for setting legends directly seem to occasionally malfunction)
        for i in range(self.labels_num):
            ax.plot([], [], [], self.visualisation_settings["path_colors"][i]+",", label=self.visualisation_settings["path_labels"][i])

        # Generate vector field plot
        if plot_vectors:
            x, y, z = np.meshgrid(
                np.linspace(self.x_min, self.x_max, vector_num),
                np.linspace(self.y_min, self.y_max, vector_num),
                np.linspace(self.z_min, self.z_max, vector_num),
            )
            
            for ind, method in enumerate(self.field_methods):
                u, v, w = utility.generate_field_vectors(vector_num, method ,x, y, z)
                ax.quiver(x, y, z, u, v, w, normalize=True, color=self.field_colors[ind], linewidth=0.5, label=method((0,0,0))[0], length=vector_plot_length)
        
        plt.legend() # Show legend
        plt.show() # Show plot

    def animate_3d(self, real_time=10, fps=20, plot_vectors=False, vector_plot_length=0, vector_num=5):
        """Uses the self.point_sets to plot and diplays an animation of the motion of all of the curves/paths

        Arguments:
            real_time: specifies real time of animation in seconds
            fps: integer specifying frame rate per second of animation
            plot_vectors: boolean value indicating whether to plot vectors or not
            vector_plot_length: length of plotted vectors (will all have the same lengths) in the scale of the plot
            vector_num: number of vectors to plot per axis direction (e.g. 5 means will plot 5*5*5 = 125 vectors per vector field)

        Assumes input point_sets have the same set of corresponding time coordinates (and a constant timestep)
        """
        # Basic setup
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        total_frames = real_time*fps
        frame_points = self.points_num / total_frames # points added per frame (can be a float value for it will be rounded when used as index)

        # Generate vector field plot
        if plot_vectors:
            x, y, z = np.meshgrid(
                np.linspace(self.x_min, self.x_max, vector_num),
                np.linspace(self.y_min, self.y_max, vector_num),
                np.linspace(self.z_min, self.z_max, vector_num),
            )
            
            for ind, method in enumerate(self.field_methods):
                u, v, w = utility.generate_field_vectors(vector_num, method ,x, y, z)
                ax.quiver(x, y, z, u, v, w, normalize=True, color=self.field_colors[ind], linewidth=0.5, label=method((0,0,0))[0], length=vector_plot_length)

        # Setting up animation path plots
        path_plots_list = []
        for color_ind in self.visualisation_settings["sets_color_ind"]:
            path_plot, = ax.plot([], [], [], self.visualisation_settings["path_colors"][color_ind]+",")
            path_plots_list.append(path_plot)

        # Setting up legend of plot with empty plots
        for i in range(self.labels_num):
            ax.plot([], [], [], self.visualisation_settings["path_colors"][i]+",", label=self.visualisation_settings["path_labels"][i])
        
        def init():
            """Init function to use as argument of animation function
            """
            ax.set_xlim(self.x_min, self.x_max)
            ax.set_ylim(self.y_min, self.y_max)
            ax.set_zlim(self.z_min, self.z_max)
            return path_plots_list

        def update(frame):
            """Update function to use as argument of animation function
            Args:
                frame: the number of the current frame (expected to start at 0 and end with the last index of the plotted points)
            Sets the new data for the plot in each frame of animation
            """
            for ind_path, path_plot in enumerate(path_plots_list):
                point_ind = round(frame_points * frame)
                path_plot.set_data(self.point_sets[ind_path][0][:point_ind], self.point_sets[ind_path][1][:point_ind])
                path_plot.set_3d_properties(self.point_sets[ind_path][2][:point_ind])
            return path_plots_list

        ani = FuncAnimation(fig, update, frames=range(total_frames), init_func=init, interval=1000/fps, blit=True) # Generate animation
        plt.legend() # Show legend
        plt.show() # Show animation
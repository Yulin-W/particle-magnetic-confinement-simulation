from simulation import Simulation
from tkinter import *
from tkinter.ttk import *
import os

# Some usage notes:
#   - Run this file to open a GUI for loading and visualising data
#   - Load file first before trying to run simulation
#   - Always at least set the plot or animation, to proportion and plot vectors field; others can be filled or left empty; if left empty default values will be used

# Initialises Simulation object
sim = Simulation()

def load_data_func():
    """Opens a window to choose data file from and loads the chosen file into sim object instance 
    """
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A Data File", filetypes=(("pkl files", "*.pkl"),))
    sim.load_data(absolute_path=filename)

def process_input(input_widget): # For processing entries that should hold floats
    """Returns float version of argument or None if the input value is empty
    """
    value = input_widget.get()
    return float(value) if value else None # returns value if value is not an empty string or None, else returns None

def process_input_int(input_widget): # For processing entries that should hold integers
    """Returns int version of argument or None if the input value is empty
    """
    value = input_widget.get()
    return int(value) if value else None # returns value if value is not an empty string or None, else returns None

def visualise_func():
    """Opens a sim visualisation of the data loaded into sim
    """
    x_min = process_input(x_min_input)
    x_max = process_input(x_max_input)
    y_min = process_input(y_min_input)
    y_max = process_input(y_max_input)
    z_min = process_input(z_min_input)
    z_max = process_input(z_max_input)
    if any([val == None for val in [x_min, x_max, y_min, y_max, z_min, z_max]]):
        custom_limits = None
    else:
        custom_limits = ((x_min, x_max), (y_min, y_max), (z_min, z_max))
    visualisation_settings = {
        "plot_or_anime" : plot_or_anime_input.get(),
        "anime_time" : process_input(anime_time_input),
        "fps" : process_input_int(fps_input),
        "to_proportion" : to_proportion_input.get() == "True",
        "custom_limits" : custom_limits,
        "plot_vectors" : plot_vectors_input.get() == "True",
        "vector_plot_length" : process_input(vector_plot_length_input),
        "vector_num" : process_input_int(vector_num_input),
    }
    settings_without_none = dict({item for item in visualisation_settings.items() if item[1] != None})
    sim.visualise(**settings_without_none)

# Initialise window
root = Tk()
root.title("Data Viewer")

# Sets GUI widgets
settings_frame = Frame(root)
settings_frame.grid(row=0, column=0)
load_data_button = Button(root, command=load_data_func, text="Load Data File")
load_data_button.grid(row=1, column=0)
visualise_button = Button(root, command=visualise_func, text="Visualise Data")
visualise_button.grid(row=2, column=0)

plot_or_anime_label = Label(settings_frame, text="Plot or Animation")
anime_time_label = Label(settings_frame, text="Animation Time (s)")
fps_label = Label(settings_frame, text="FPS")
to_proportion_label = Label(settings_frame, text="To Proportion")
custom_limits_label = Label(settings_frame, text="Custom Limits")
plot_vectors_label = Label(settings_frame, text="Plot Vectors")
vector_plot_length_label = Label(settings_frame, text="Vector Plot Length")
vector_num_label = Label(settings_frame, text="Number of Vectors Per Axis")

plot_or_anime_input = Combobox(settings_frame, values=["plot", "anime"])
plot_or_anime_input.current(0)
anime_time_input = Entry(settings_frame)
fps_input = Entry(settings_frame)
to_proportion_input = Combobox(settings_frame, values=[True, False])
to_proportion_input.current(0)
custom_limits_input = Frame(settings_frame)
x_min_input = Entry(custom_limits_input)
x_max_input = Entry(custom_limits_input)
y_min_input = Entry(custom_limits_input)
y_max_input = Entry(custom_limits_input)
z_min_input = Entry(custom_limits_input)
z_max_input = Entry(custom_limits_input)
plot_vectors_input = Combobox(settings_frame, values=[True, False])
plot_vectors_input.current(1)
vector_plot_length_input = Entry(settings_frame)
vector_num_input = Entry(settings_frame)

plot_or_anime_label.grid(row=0, column=0)
anime_time_label.grid(row=1, column=0)
fps_label.grid(row=2, column=0)
to_proportion_label.grid(row=3, column=0)
custom_limits_label.grid(row=4, column=0)
plot_vectors_label.grid(row=5, column=0)
vector_plot_length_label.grid(row=6, column=0)
vector_num_label.grid(row=7, column=0)

plot_or_anime_input.grid(row=0, column=1)
anime_time_input.grid(row=1, column=1)
fps_input.grid(row=2, column=1)
to_proportion_input.grid(row=3, column=1)
custom_limits_input.grid(row=4, column=1)
x_min_input.grid(row=0, column=0)
x_max_input.grid(row=0, column=1)
y_min_input.grid(row=1, column=0)
y_max_input.grid(row=1, column=1)
z_min_input.grid(row=2, column=0)
z_max_input.grid(row=2, column=1)
plot_vectors_input.grid(row=5, column=1)
vector_plot_length_input.grid(row=6, column=1)
vector_num_input.grid(row=7, column=1)

# Runs GUI
root.mainloop()

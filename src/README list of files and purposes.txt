1. Python scripts
	em.py: contains classes representing charged particles and force fields; includes particle-field interaction and particle time step update methods
	simulation.py: contains a Simulation class used to generate data, output data, load data, visualise data (via calling methods of a Visualiser class instance)
	visualisation.py: contains a Visualiser class used to visualise data, generate plots, generate animations, draw vector fields
	utility.py: contains useful constants and functions
	data_viewer.py: GUI for making loading and visualising data more convenient
	small_value_deuterium_tokamak_data_generator.py: data sample generation for tokamaks with small variable values
	iter_tokamak_data_generator.py: data sample generation for tokamaks modelled after ITER
	case_data_generator.py: data generation for single particle simulations where individual drift velocities involved in a tokamak are isolated
2. Data Folders
	Data Plot Images: contains images of plots from confinement_time_analysis.ipynb
	General Data: contains data of single-particle simulations
	ITER Tokamak Data: contains data of sets of multi-particle tokamaks simulations modelled after ITER used in the report
	ITER Tokamak Test Case Data: contains data of some individual ITER based tokamak test cases for probing behaviour
	Path Plot Images: contains images of path plots of individual drift velocities of charges in corresponding fields conditions (data_viewer can be used to generate more interactive path plots and also animations)
	Processed Data in Excel Format: contains data exported to excel format from confinement_time_analysis.ipynb
	Small Value Tokamak Data: contains data of multi-particle small value tokamak simulations used in the report 
3. Other
	confinement_time_analysis.ipynb: contains important data, statistics, plots, simulation settings for the 4 sets of multi-particle simulations from the folders ITER Tokamak Data and Small Value Tokamak Data

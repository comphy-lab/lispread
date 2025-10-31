import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity
from libraries.create_all_plots import create_all_plots_power05, create_all_plots_linear
# basic variables

# physical constants for comparison to paper
R, rho, gamma, g, h = 0.65e-3, 1e3, 0.072, 9.81, 0.05

# get folder names



t_end = np.array([
           1.2,
           1.5,
           1.5,
           1.5,
           3,
           3,
           3,
           3,
           3
])


print("\n\n old 1::")
create_all_plots_linear(load_folders(["/media/mark/Markinator/Simulations/Old_ohnesorge_number_results"]),fig_save_dir= "figures/Oh_comparison/old_Oh/forced/power1/", forced_exponent=1 ,
                        forced_dt=0, t_end=t_end, plot_individual_plots=True, h=0.1)

print("\n\n new 1:")
create_all_plots_linear(load_folders(["/media/mark/Markinator/Simulations/New_ohnesorge_number_results"]),fig_save_dir= "figures/Oh_comparison/new_Oh/forced/power1/", forced_exponent=1 ,
                        forced_dt=0, t_end=t_end, plot_individual_plots=True, h=0.1)
plt.close('all')
print("\n\n old 0.5:")

create_all_plots_power05(load_folders(["/media/mark/Markinator/Simulations/Old_ohnesorge_number_results"]),fig_save_dir= "figures/Oh_comparison/old_Oh/forced/power0p5/", forced_exponent=0.5 ,
                        forced_dt=None, t_end=t_end, plot_individual_plots=True, h=0.1)
print("\n\n new 0.5:")

create_all_plots_power05(load_folders(["/media/mark/Markinator/Simulations/New_ohnesorge_number_results"]),fig_save_dir= "figures/Oh_comparison/new_Oh/forced/power0p5/", forced_exponent=0.5 ,
                        forced_dt=None, t_end=t_end, plot_individual_plots=True, h=0.1)
plt.close('all')



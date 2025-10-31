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
forced_fit = True
plot_individual_plots = True

folder_names=["2025_10_01_results copy", "2025_10_01_results", "Compare_OH_methods"]


# physical constants for comparison to paper
# R, rho, gamma, g, h = 0.65e-3, 1e3, 0.072, 9.81, 0.05
# print(1/h**0.5)
# print("max_Oh_paper = ", 1/np.sqrt(rho*R*gamma))
# print("96 mPa viscosityOh_paper = ", 0.096/np.sqrt(rho*R*gamma))

# get folder names
folders = load_folders(folder_names)



t_end = np.array([
           1.4,     # 0.001
           1.4,    # 0.01
           1.4,      # 0.02
           1.4,    # 0.08
           1.4,     # 0.2
           1.4,       # 0.44
           1.4, 
           2,# 2,       # 1
           4,# 4,       # 2.5
           5,       # 5
           20])       # 20


create_all_plots_linear(folders,fig_save_dir="figures/Expansion behaviour/power1/unforced1/", forced_exponent=None ,
                        forced_dt=None, t_end=t_end, plot_individual_plots=True, h=0.05)
plt.close('all')
create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/power0p5/unforced0p5/", 
                        forced_exponent=None, forced_dt=None, t_end=t_end, plot_individual_plots=True, h=0.05)
plt.close('all')
create_all_plots_linear(folders,fig_save_dir="figures/Expansion behaviour/power1/forced1/", forced_exponent=1, 
                        forced_dt=None, t_end=t_end, plot_individual_plots=True, h=0.05)
plt.close('all')
create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/power0p5/forced0p5/", 
                        forced_exponent=0.5, forced_dt=None, t_end=t_end, plot_individual_plots=True, h=0.05)
plt.close('all')


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels
from libraries.create_glycerol_plots import create_glycerol_plots


plt.close('all')

# forced_dt = [0] * 3
forced_dt=[0]*3
forced_dt=[0] * 3
forced_dt=[3]*2.5
# forced_dt = None
# save_plots=False
folders = load_folders(["glycerol/0p03/"])
        
create_glycerol_plots(folders,fig_save_dir="figures/glycerol/",
                        forced_dt=forced_dt, plot_individual_plots=False, h=0.03, save_plots=True)

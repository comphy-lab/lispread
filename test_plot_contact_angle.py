import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity
from libraries.create_all_plots import create_all_plots_power05, create_all_plots_linear

t, z, r, v, theta1, theta2 = load_data("test")
create_plot(t, theta1 * 180/np.pi, 1)
save_plot(1, "test/testcontact_angle.png")
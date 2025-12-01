import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels
from libraries.create_bubble_plots import create_bubble_plots

def create_all_triangles():
    plot_triangle_with_labels((2*1e-2*2, 0.3) , (2*1e-2*2, 0.6), (2*1e-2*2**2*2, 0.6), figure=4, l1=1, l2=2,
    l1_center = ["right", "top"], l2_center = ["right", "bottom"])
    plot_triangle_with_labels((3*1e-2*2, 0.3) , (3*1e-2*2, 0.6), (3*1e-2*2**2*2, 0.6), figure=5, l1=1, l2=2,
    l1_center = ["right", "top"], l2_center = ["right", "bottom"])
    plot_triangle_with_labels((100 * 1, 0.38 ) , (100 * 3, 0.38), (100 * 3, 0.38*3**-1 ), figure=99, l1=1, l2=1,
    l1_center = ["right", "bottom"], l2_center = ["right", "top"])

plt.close('all')
create_all_triangles()

t_end= [0.75, 0.8, 1, 1.5, 2, 2, 2.5, 3]

t_plot = [0.75, 0.8, 1, 50,50,50,50,50]
# forced_dt = np.array([
#     0.02,     
#     0.025,
#     0.043, 
#     0.08, 
#     0.12, 
#     0.22,
#     0.35, 
#     1])
# forced_dt = np.array([
# 0.015,     
# 0.02,
# 0.043, 
# 0.08, 
# 0.125, 
# 0.24,
# 0.42, 
# None])
forced_dt = np.array([
0.02,     
0.027,
0.048, 
0.086, 
0.135, 
0.26,
0.46, 
None])
folders = load_folders(["/media/markEnAman/BackupNator/discoverer/bubble2"])
folders =[f for f in folders if "2025_11_13_" in f]
print(folders)
create_bubble_plots(folders,fig_save_dir="figures/bubble/", t_end=t_end, t_plot=t_plot, forced_exponent=0.5,
                        forced_dt=forced_dt, plot_individual_plots=False, h=0.05, save_plots=True)

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels
from libraries.create_droplet_mastercurve import create_mastercurve_plots #create_all_plots_power05, create_all_plots_linear, 





plt.close('all')


forced_exponent = 0.5  # set to None for automatic exponent fitting
i = 0
colors = ["b", "r", "g"]
save_plots=False
temp_folder_names=load_folders(["/media/markEnAman/BackupNator/discoverer/water"])
# print(temp_folder_names)
folder_dict = {}
for folder in temp_folder_names:
    if "_hf_0p05" not in folder:
        continue
    hf_raw = re.search(r"_hf_([^_]+)", folder).group(1)
    skip_Oh=[0.001, 5]
    # convert '0p05' to '0.05'
    hf_value = float(hf_raw.replace("p", "."))
    if hf_value not in folder_dict:
        folder_dict[hf_value] = []

    folder_dict[hf_value].append(folder)
print(folder_dict.keys())
marker = "o" + colors[i-1]
save_plots = True
for key in folder_dict.keys():
    h = float(key)
    folders = folder_dict[key]

    t_end =  [np.inf]*100

    forced_dt = np.array([
            0,
            0.014719897344058892, 
            0.025178255897390405, 
            0.07502022304381205, 
            0.1812777531071097, 
            0.3216676611763525, 
            0.68595360350302, 
            1.2183242194293438])
    forced_dt[1] += 0.01   # orange
    forced_dt[2] += 0.01   # green
    forced_dt[3] += 0.01   # red
    forced_dt[4] += -0.005   # purple
    forced_dt[5] += -0.005   # brown
    forced_dt[6] += -0.03   # pink
    forced_dt[7] += -0.01   # gray
    rc = np.array([ None,
    0.85,   # orange
    0.95,   # green
    1,   # red
    1,   # purple
    1,  # brown
    1,   # pink
    1   # gray
    ])
    tauc = np.array([ None,
    0.4,   # orange
    0.6,   # green
    1,   # red
    1.3,   # purple
    1.8,  # brown
    4,   # pink
    1   # gray
    ])
    # forced_dt*=0
    # forced_dt[1] += 0.003   # orange
    # forced_dt[2] += 0.008   # green
    # forced_dt[3] += 0.025   # red
    # forced_dt[4] += 0.05   # purple
    # forced_dt[5] += 0.07   # brown
    # forced_dt[6] += 0.08   # pink
    # forced_dt[7] += 0   # gray
    tauc[1] *= 1/2   # orange
    tauc[2] *= 1/2   # green
    tauc[3] *= 1/2   # red
    tauc[4] *= 1   # purple
    tauc[5] *= 1   # brown
    tauc[6] *= 1   # pink
    tauc[7] *= 1   # gray
    r_fitrange = [(0.16, 0.6)] + [(0.16, 0.7)]*2 +[(0.17,0.7)]+ [(0.2, 0.7)]*5
    create_mastercurve_plots(folders, fig_save_dir="figures/water/mastercurve/", forced_exponent=forced_exponent ,
                            forced_dt=forced_dt, t_end=t_end, plot_individual_plots=False, h=h, save_plots=save_plots, 
                            linestyle=".", marker=marker, skip_Oh=skip_Oh, rc=rc, tauc=tauc)
    

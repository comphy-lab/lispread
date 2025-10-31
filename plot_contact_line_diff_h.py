import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels
from libraries.create_all_plots import create_all_plots_power05, create_all_plots_linear





plt.close('all')
i = 0
save_plots=False
linestyles = [":", "-.", "--"]
Oh_list = [0.001, 0.01, 0.06, 0.2, 0.5, 1, 2.5, 5, 20]
h_list = [0.03, 0.05, 0.1]
cmap = plt.get_cmap("tab10")
colors = [cmap(i % 10) for i, ohf in enumerate(Oh_list)]
n_figs = [2, 3, 4, 5, 11, 10]
savenames = ["rvst_originol.png", "rvst_originol_log.png", "rvst_corrected_log.png", "rvstD_corrected_log.png", "vvst_original.png", "vvst_filtered.png"]


def create_all_triangles():
    plot_triangle_with_labels((0.03, 0.04) , (0.03, 0.1), (0.03 * (0.1/0.04)**(1/1), 0.1), figure=1, l1=5, l2=1)
    plot_triangle_with_labels((0.2, 0.6) , (0.2, 0.9), (0.2 * (0.9/0.6)**(1/0.5), 0.9), figure=3, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
    plot_triangle_with_labels((1, 0.03) , (3, 0.03), (3, 0.03 * 3/1), figure=3, l1=1, l2=1,
    l1_center = ["right", "top"], l2_center = ["left", "top"])
    plot_triangle_with_labels((0.1, 5e-2) , (0.1, 0.4), (0.1*0.4/5e-2, 0.4), figure=4, l1=1, l2=1)
    plot_triangle_with_labels((1, 0.6) , (1, 1.1), (1.1/0.6*2, 1.1), figure=4, l1=1, l2=2)
    plt.xlim(8e-2, None)
    plot_triangle_with_labels((0.08, 0.1) , (0.08, 0.4), (0.04*0.4/5e-2, 0.4), figure=5, l1=1, l2=1)
    plot_triangle_with_labels((0.5, 0.6) , (0.5, 1.1), (0.5*1.1/0.6*2, 1.1), figure=5, l1=1, l2=2)
    plt.xlim(1e-2, 3)
    plot_triangle_with_labels((1, 0.4) , (1,  0.8), (0.5, 0.8), figure=11, l1=1, l2=1)
    # plt.xlim(1e-2, 3)
    plot_triangle_with_labels((0.5, 0.8), (1.1, 0.8), (1.1, 0.8*(1.1/0.5)**-0.75), figure=10, l1=3, l2=4)
    # plt.xlim(1e-2, 3)
    # plt.ylim(1.1/(3/1e-2), 1.1)
    # plot_triangle_with_labels((0.6, 0.6), (1, 0.6), (1, 0.6*(1/0.6)**-1), figure=10, l1=1, l2=2)
    # plot_triangle_with_labels((2e-1, 0.3) , (2e-1, 0.1), (2e-1*3/0.75, 0.1), figure=11, l1=3, l2=4)
    # plot_triangle_with_labels((2e-1, 0.3) , (2e-1, 0.1), (2e-1*3/0.6, 0.1), figure=11, l1=1, l2=1)
    plt.gca().set_aspect('equal', adjustable='box')


for hf_string in ["0p03", "0p05", "0p1"]:
    i += 1
    if i==3:
        save_plots = True
    h = float(hf_string.replace("p", "."))
    folder_names=["2025_10_17_hf_" + hf_string]
    # get folder names
    folders = load_folders(folder_names)
    t_end = np.array([20] * 5 + [1.1, 20, 20, 20])
    create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf_all/power0p5/forced0p5/", 
                            forced_exponent=0.5, forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, save_plots=save_plots, linestyle=linestyles[i-1])
   

i = 0
plot_triangle_with_labels((0.1, 0.4) , (0.1, 2*0.4), (0.3, 2*0.4), figure=3, l1=1, l2=2)
plot_triangle_with_labels((1, 0.05) , (5, 0.05), (5, 0.05*5), figure=3, l1=1, l2=1)
for i in range(len(n_figs)):
    make_Oh_h_legend(Oh=Oh_list, h=h_list, colors=colors, linestyles=linestyles, n_fig=n_figs[i])
    save_plot(n_figs[i], "figures/Expansion behaviour/2025_10_17/hf_all/power0p5/forced0p5/"+savenames[i])
    


i = 0
save_plots=False
for hf_string in ["0p03", "0p05", "0p1"]:
    i += 1
    if i==3:
        save_plots = True
    h = float(hf_string.replace("p", "."))
    folder_names=["2025_10_17_hf_" + hf_string]
    # get folder names
    folders = load_folders(folder_names)
    t_end = np.array([20] * 5 + [1.1, 20, 20, 20])
    create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf_all/power0p5/unforced0p5/", 
                            forced_exponent=None, forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, save_plots=save_plots, linestyle=linestyles[i-1])

i = 0
for i in range(len(n_figs)):
    make_Oh_h_legend(Oh=Oh_list, h=h_list, colors=colors, linestyles=linestyles, n_fig=n_figs[i])
    save_plot(n_figs[i], "figures/Expansion behaviour/2025_10_17/hf_all/power0p5/unforced0p5/"+savenames[i])
plt.close('all')
i = 0
save_plots=False
create_all_triangles()
for hf_string in ["0p03", "0p05", "0p1"]:
    i += 1
    if i==3:
        save_plots = True
    h = float(hf_string.replace("p", "."))
    folder_names=["2025_10_17_hf_" + hf_string]
    # get folder names
    folders = load_folders(folder_names)
    t_end = np.array([20] * 4 + [1.5, 1.5, 20, 20, 20])
    create_all_plots_linear(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf_all/power1/forced1/", 
                            forced_exponent=1, forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, save_plots=save_plots, linestyle=linestyles[i-1], skip_Oh=[])


create_all_triangles()
i = 0
for i in range(len(n_figs)):
    make_Oh_h_legend(Oh=Oh_list, h=h_list, colors=colors, linestyles=linestyles, n_fig=n_figs[i])
    save_plot(n_figs[i], "figures/Expansion behaviour/2025_10_17/hf_all/power1/forced1/"+savenames[i])
plt.close('all')

i = 0
save_plots=False
for hf_string in ["0p03", "0p05", "0p1"]:
    i += 1
    if i==3:
        save_plots = True
    h = float(hf_string.replace("p", "."))
    folder_names=["2025_10_17_hf_" + hf_string]
    # get folder names
    folders = load_folders(folder_names)
    t_end = np.array([20] * 5 + [1.1, 20, 20, 20])
    create_all_plots_linear(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf_all/power1/unforced1/", 
                            forced_exponent=None, forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, save_plots=save_plots, linestyle=linestyles[i-1])
i = 0
for i in range(len(n_figs)):
    make_Oh_h_legend(Oh=Oh_list, h=h_list, colors=colors, linestyles=linestyles, n_fig=n_figs[i])
    save_plot(n_figs[i], "figures/Expansion behaviour/2025_10_17/hf_all/power1/unforced1/"+savenames[i])
plt.close('all')


i = 0
for hf_string in ["new", "0p03", "0p05", "0p1"]:
    if hf_string == "new":
        h = 0.03
        folder_names=["2025_10_17"]
        hf_string = "0p03MaxLevel12"
    else:
        h = float(hf_string.replace("p", "."))
        folder_names=["2025_10_17_hf_"+hf_string]


    # physical constants for comparison to paper

    # get folder names
    folders = load_folders(folder_names)



    t_end = np.array(([1.1] * 5 + [1.1, 20, 20, 20])*2)

    create_all_triangles()
    create_all_plots_linear(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf"+hf_string+"/power1/unforced1/", forced_exponent=None ,
                            forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h)
    plt.close('all')
    create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf"+hf_string+"/power0p5/unforced0p5/", 
                            forced_exponent=None, forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h)
    plt.close('all')
    create_all_triangles()
    create_all_plots_linear(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf"+hf_string+"/power1/forced1/", forced_exponent=1.5, 
                            forced_dt=0, t_end=t_end, plot_individual_plots=False, h=h)
    plt.close('all')
    create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf"+hf_string+"/power0p5/forced0p5/", 
                            forced_exponent=0.5, forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h)
    plt.close('all')


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels
from libraries.create_all_plots import create_all_plots #create_all_plots_power05, create_all_plots_linear, 





plt.close('all')
i = 0
save_plots=False
linestyles_Oh = [":", "-.", "--"]
linestyles= linestyles_Oh * 2
Oh_list = [0.001, 0.01, 0.06, 0.2, 0.5, 1, 2.5, 5, 20]
h_list = [0.1, 0.05, 0.03]
cmap = plt.get_cmap("tab10")
colors_Oh = [cmap(i % 10) for i, ohf in enumerate(Oh_list)]
n_figs = [2, 3, 4, 5, 11, 10, 444, 124]
savenames = ["rvst_originol.png", "rvst_originol_log.png", "rvst_corrected_log.png", "rvstD_corrected_log.png", 
            "vvst_original.png", "vvst_filtered.png", "rvst_collapsed.png", "tmsvsrmum.png"]

# for i in range(len(n_figs)):
#     make_Oh_h_legend(Oh=Oh_list, h=h_list, colors=colors_Oh, linestyles=linestyles, n_fig=n_figs[i])
#     save_plot(n_figs[i], "figures/Expansion behaviour/2025_10_17/hf_all/power1/unforced1/"+savenames[i])
plt.close('all')


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
    plot_triangle_with_labels((0.5, 0.8*650), (1.1, 0.8*650), (1.1, 0.8*(1.1/0.5)**-0.75*650), figure=10, l1=3, l2=4)
    plot_triangle_with_labels((0.2*0.5, 0.6*650) , (0.2*0.5, 0.9*650), (0.2 * (0.9/0.6)**(1/0.5)*0.5, 0.9*650), figure=124, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
    plot_triangle_with_labels((1*0.5, 0.03*650) , (3*0.5, 0.03*650), (3*0.5, 0.03 * 3/1*650), figure=124, l1=1, l2=1,
    l1_center = ["right", "top"], l2_center = ["left", "top"])
    plot_triangle_with_labels((1e-2, 0.2) , (1e-2, 0.5), (1e-2 * (0.5/0.2)**(2), 0.5), figure=444, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
    # plt.xlim(1e-2, 3)
    # plt.ylim(1.1/(3/1e-2), 1.1)
    # plot_triangle_with_labels((0.6, 0.6), (1, 0.6), (1, 0.6*(1/0.6)**-1), figure=10, l1=1, l2=2)
    # plot_triangle_with_labels((2e-1, 0.3) , (2e-1, 0.1), (2e-1*3/0.75, 0.1), figure=11, l1=3, l2=4)
    # plot_triangle_with_labels((2e-1, 0.3) , (2e-1, 0.1), (2e-1*3/0.6, 0.1), figure=11, l1=1, l2=1)
    # plt.gca().set_aspect('equal', adjustable='box')

# for sdir, region, forced_exponent in zip(["/power1/forced1/", "/power0p5/forced0p5/", "/power1/unforced1/", "/power0p5/unforced0p5/"], 
#                                          [1, 2, 1, 2], [1, 0.5, None, None]): 
for sdir, region, forced_exponent in zip(["/power0p5/forced0p5/", "/power0p5/unforced0p5/"], 
                                         [2, 2], [0.5, None]): 
    i = 0
    colors = ["b", "r", "g"]
    save_plots=False
    for hf_string in ["0p05MaxLevel12"]:#["0p1MaxLevel12", "0p05MaxLevel12", "0p03MaxLevel12"]:#, "0p1", "0p05", "0p03"]:
        folder_names=["water/2025_10_17_hf_" + hf_string]
        if hf_string[-10:] == "MaxLevel12":
            h = float(hf_string[:-10].replace("p", "."))
            skip_Oh = []
        else:
            h = float(hf_string.replace("p", "."))
            if h == 0.1:
                skip_Oh = [0.001]

        i += 1
        if i>3:
            marker = "x" + colors[i-4]
        else:
            marker = "o" + colors[i-1]
        if i == 1:
            save_plots=True
        # get folder names
        folders = load_folders(folder_names)
        t_end =  [np.inf]*100
            
        create_all_plots(folders,fig_save_dir="figures/water/Expansion behaviour/2025_10_17/hf_all"+sdir, forced_exponent=forced_exponent ,
                                forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, save_plots=save_plots, 
                                linestyle=linestyles[i-1], marker=marker, skip_Oh=skip_Oh)
        # create_all_plots_power05(folders,fig_save_dir="figures/Expansion behaviour/2025_10_17/hf_all"+sdir, forced_exponent=forced_exponent ,
        #                         forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, region=region, save_plots=save_plots)
        if save_plots:
            create_all_triangles()
            # i = 0
            # plot_triangle_with_labels((0.1, 0.4) , (0.1, 2*0.4), (0.3, 2*0.4), figure=3, l1=1, l2=2)
            # plot_triangle_with_labels((1, 0.05) , (5, 0.05), (5, 0.05*5), figure=3, l1=1, l2=1)
            for i in range(len(n_figs)):
                make_Oh_h_legend(Oh=Oh_list, h=h_list, colors=colors_Oh, linestyles=linestyles_Oh, n_fig=n_figs[i])
                save_plot(n_figs[i], "figures/water/Expansion behaviour/2025_10_17/hf_all"+sdir+savenames[i])

            plt.figure(99)    
            handles, labels = [], []
            ax = plt.gca()

            handles.append(plt.Line2D([0], [0], color="black", marker="x", linestyle="none",
            markerfacecolor='none', markeredgewidth=1))
            labels.append(r"grid refinement level 11")
            handles.append(plt.Line2D([0], [0], color="black", marker="o", linestyle="none",
            markerfacecolor='none', markeredgewidth=1))
            labels.append(r"grid refinement level 12")
            handles.append(plt.Line2D([0], [0], color="black", marker="s", linestyle="none",
            markerfacecolor='none', markeredgewidth=1))
            labels.append(r"Experiments (Nath & Quéré)")
            if region ==1:
                handles.append(plt.Line2D([0], [0], color="black", linestyle="--"))
                labels.append(r"$\tilde u_r \sim 1$")
                handles.append(plt.Line2D([0], [0], color="black", linestyle=":"))
                labels.append(r"$\tilde u_r \sim Oh^{-1}$")
            if region ==2:
                handles.append(plt.Line2D([0], [0], color="black", linestyle="--"))
                labels.append(r"$\frac{D}{D_0} \sim 1$")
                handles.append(plt.Line2D([0], [0], color="black", linestyle=":"))
                labels.append(r"$\frac{D}{D_0} \sim\left(Oh(\frac{R}{h})\right)^{-1}$")
            for i in range(len(h_list)):
                handles.append(plt.Line2D([0], [0], color=colors[i], marker="o", linestyle="none"))
                labels.append(f"$h = {h_list[i]}$")
            
            ax.legend([])  # This removes the original legend
            ax.legend(handles=handles, labels=labels, loc='best', fontsize=14, markerscale=1.5,)# Add the custom legend
            save_plot(99, "figures/water/Expansion behaviour/2025_10_17/hf_all"+sdir+"DvsOh.png")
            
            plt.figure(63)    
            handles, labels = [], []
            ax = plt.gca()

            handles.append(plt.Line2D([0], [0], color="black", marker="x", linestyle="none",
            markerfacecolor='none', markeredgewidth=1))
            labels.append(r"grid refinement level 11")
            handles.append(plt.Line2D([0], [0], color="black", marker="o", linestyle="none",
            markerfacecolor='none', markeredgewidth=1))
            labels.append(r"grid refinement level 12")
            for i in range(len(h_list)):
                handles.append(plt.Line2D([0], [0], color=colors[i], marker="o", linestyle="none"))
                labels.append(f"$h = {h_list[i]}$")
            
            ax.legend([])  # This removes the original legend
            ax.legend(handles=handles, labels=labels, loc='best', fontsize=14, markerscale=1.5,)# Add the custom legend
            save_plot(63, "figures/water/Expansion behaviour/2025_10_17/hf_all"+sdir+"exponentvsOH.png")
            

            plt.close('all')


for hf_string in ["0p03MaxLevel12", "0p05MaxLevel12", "0p1MaxLevel12", "0p03", "0p05", "0p1"]:
    folder_names=["water/2025_10_17_hf_"+hf_string]
    if hf_string[-10:] == "MaxLevel12":
        h = float(hf_string[:-10].replace("p", "."))
    else:
        h = float(hf_string.replace("p", "."))


    # physical constants for comparison to paper

    # get folder names
    folders = load_folders(folder_names)
    t_end = np.array(([1.1] * 5 + [1.1, 20, 20, 20])*2)
    i = 0
    #for sdir, region, forced_exponent in zip(["/power0p5/forced0p5/", "/power1/forced1/", "/power1/unforced1/", "/power0p5/unforced0p5/"], [2, 1, 1, 2], [0.5, 1, None, None]): 
    for sdir, region, forced_exponent in zip(["/power0p5/forced0p5/", "/power0p5/unforced0p5/"], [2, 2], [0.5, None]): 
        print("-------------------------------------------------------------------------\nsaving to",hf_string+sdir + "\n-------------------------------------------------------------------------")
        if i%2 ==0:
            """
            """
            create_all_triangles()
        create_all_plots(folders,fig_save_dir="figures/water/Expansion behaviour/2025_10_17/hf"+hf_string+sdir, forced_exponent=forced_exponent ,
                                forced_dt=None, t_end=t_end, plot_individual_plots=False, h=h, region=region)
        plt.close('all')
        i += 1
        


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
import json
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels
from libraries.create_all_plots_diff_OHd import create_all_plots #create_all_plots_power05, create_all_plots_linear, 
def create_all_triangles():
    plot_triangle_with_labels((0.03, 0.04) , (0.03, 0.1), (0.03 * (0.1/0.04)**(1/1), 0.1), figure=1, l1=5, l2=1)
    plot_triangle_with_labels((0.2, 0.6) , (0.2, 0.9), (0.2 * (0.9/0.6)**(1/0.5), 0.9), figure=3, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
    plot_triangle_with_labels((1, 0.03) , (3, 0.03), (3, 0.03 * 3/1), figure=3, l1=1, l2=1,
    l1_center = ["right", "top"], l2_center = ["left", "top"])
    plot_triangle_with_labels((0.1, 5e-2) , (0.1, 0.4), (0.1*0.4/5e-2, 0.4), figure=4, l1=1, l2=1)
    plot_triangle_with_labels((1, 0.6) , (1, 1.1), (1.1/0.6*2, 1.1), figure=4, l1=1, l2=2)
    plt.xlim(8e-2, None)
    plot_triangle_with_labels((0.08 / 5, 0.1/2) , (0.04*0.4/5e-2 /5, 0.1/2), (0.04*0.4/5e-2 / 5, 0.4/2), figure=5, l1=1, l2=1)

    plot_triangle_with_labels((0.2 * 0.5, 0.6) , (0.2 * 0.5, 1.1), (0.2 * 0.5*1.1/0.6*2, 1.1), figure=5, l1=1, l2=2)
    # plt.xlim(1e-2, 3)
    plot_triangle_with_labels((1, 0.4) , (1,  0.8), (0.5, 0.8), figure=11, l1=1, l2=1)
    # plt.xlim(1e-2, 3)
    plot_triangle_with_labels((0.5, 0.8*650), (1.1, 0.8*650), (1.1, 0.8*(1.1/0.5)**-0.75*650), figure=10, l1=3, l2=4)
    plot_triangle_with_labels((0.2*0.5, 0.6*650) , (0.2*0.5, 0.9*650), (0.2 * (0.9/0.6)**(1/0.5)*0.5, 0.9*650), figure=124, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
    plot_triangle_with_labels((1*0.5, 0.03*650) , (3*0.5, 0.03*650), (3*0.5, 0.03 * 3/1*650), figure=124, l1=1, l2=1,
    l1_center = ["right", "top"], l2_center = ["left", "top"])
    plot_triangle_with_labels((1e-2*2.5, 0.2) , (1e-2*2.5, 0.5), (2.5* 1e-2 * (0.5/0.2)**(2), 0.5), figure=444, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])

    plot_triangle_with_labels((1, 0.08) , (3, 0.08), (3, 0.08*3), figure=444, l1=1, l2=1,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])

    # plot_triangle_with_labels((200 * 2,7.5e-2) , (500* 2, 7.5e-2), (500* 2, 3e-2), figure=99, l1=1, l2=1,
    # l1_center = ["right", "bottom"], l2_center = ["right", "top"])
    # plt.xlim(1e-3, 1e3)

linestyles_Oh = [":", ".-", "--"]
linestyles= linestyles_Oh * 2
Oh_list = [0.001, 0.01, 0.06, 0.2, 0.5, 1, 2.5, 5, 20]
h_list = [0.03, 0.05, 0.1]
cmap = plt.get_cmap("tab10")
colors_Oh = [cmap(i % 10) for i, ohf in enumerate(Oh_list)]
n_figs = [2, 3, 4, 5, 11, 10, 444, 124]
savenames = ["rvst_originol.png", "rvst_originol_log.png", "rvst_corrected_log.png", "rvstD_corrected_log.png", 
            "vvst_original.png", "vvst_filtered.png", "rvst_collapsed.png", "tmsvsrmum.png"]
Oh_d_list = []
Oh_f_list = []
h_list = []
D_list = []
t_start_list = []
plt.close('all')

main_directory = "/media/markEnAman/Mark1000/discoverer"

forced_dt = None
folders = [main_directory + "/" + d for d in os.listdir(main_directory) if d[0]=="1" ] 

temp_folder_names=load_folders(folders)
# print(temp_folder_names)
folder_dict = {}
save_plots = True
for folder in temp_folder_names:
    # if "2025_13_10_" not in folder:
    #     continue
    hf_raw = re.search(r"_hf_([^_]+)", folder).group(1)
    
    # convert '0p05' to '0.05'
    hf_value = float(hf_raw.replace("p", "."))
    if hf_value not in folder_dict:
        folder_dict[hf_value] = []
    folder_dict[hf_value].append(folder)
print(folder_dict.keys())    
# forced_dt = [
#     0.0203,                                     #0
#     0.021,                                      #1
#     0.022,                                      #2
#     0.023,                                      #3
#     0.028,                                      #4                                     #0
#     0.029,                                      #5
#     0.03,                                      #6
#     0.032,                                      #7
#     0.066,                                      #8
#     0.069,                                      #9
#     0.071,                                      #10
#     0.075,                                      #11
#     0.163,                                      #12
#     0.169,                                      #13
#     0.176,                                      #14
#     0.183,                                      #15
#     0.291,                                      #16
#     0.316,                                      #17
#     0.324,                                      #18
#     0.342,                                      #19
#      100, #0.342,                                      #20
#      100, #0.584,                                      #21
#     0.810,                                      #22
#      100, #0.840,                                      #23
#      100, #0.840,                                      #24
#      100, #0.3869153736152997,                                      #25
#      100, #1e-10,                                      #26
#      None,                                      #27
#      100, #1.7177378798291996,                                     #0                                     #0
#      100, #0,
#      100, #0,
#      100]
# forced_dt = None
for key in folder_dict.keys():
    h = float(key)
    print(h)
    forced_dt = [
    0.0203,                                     #0
    0.021,                                      #1
    0.022,                                      #2
    0.023,                                      #3
    0.028,                                      #4                                     #0
    0.029,                                      #5
    0.03,                                      #6
    0.032,                                      #7
    0.066,                                      #8
    0.069,                                      #9
    0.071,                                      #10
    0.075,                                      #11
    0.163,                                      #12
    0.169,                                      #13
    0.176,                                      #14
    0.183,                                      #15
    0.291,                                      #16
    0.316,                                      #17
    0.324,                                      #18
    0.342,                                      #19
     100, #0.342,                                      #20
     100, #0.584,                                      #21
    0.810,                                      #22
     100, #0.840,                                      #23
     100, #0.840,                                      #24
     100, #0.3869153736152997,                                      #25
     100, #1e-10,                                      #26
     None,                                      #27
     100, #1.7177378798291996,                                     #0                                     #0
     100, #0,
     100, #0,
     100]
    for i in range(len(forced_dt)):
        forced_dt[i] = None
    if h==0.006:
        for i in [17, 18,19, 20, 21, 23, 24, 25, 26, 28, 29, 30]:
            forced_dt[i] = 100
    elif h ==0.015:
        for i in [20, 21, 23, 24, 25, 26, 28, 29, 30]:
            forced_dt[i] = 100
    elif h==0.03:
        for i in [23, 24, 25, 26, 28, 29, 30]:
            forced_dt[i] = 100
    elif h==0.05:
        for i in [23, 24, 25, 26, 28, 29, 30]:
            forced_dt[i] = 100




    Ohd_raw = re.search(r"_Ohd_([^_]+)", folder).group(1)
    create_all_triangles()
    # convert '0p05' to '0.05'
    Ohd_value = float(Ohd_raw.replace("p", "."))

    folders = folder_dict[key]
    print([d.split("/")[-1][:4] for d in folders])
    r_fitrange = [(0.16, 0.6)]*8 + [(0.16, 0.7)]*8 +[(0.17,0.7)]*4+ [(0.2, 0.7)]*4 + [(0.25, 0.7)]*16
    
    # if h == 0.006:
    #     create_all_plots(folders, fig_save_dir="figures/water/diffOhDrop/", forced_exponent=0.5 ,
    #                     forced_dt=None, t_end=None, plot_individual_plots=False, h=h, save_plots=True, 
    #                         r_fitrange=r_fitrange)
    #     continue

    Ohf_, D_, t_start_, h_, Ohd_ = create_all_plots(folders, fig_save_dir="figures/water/diffOhDrop/", forced_exponent=0.5 ,
                            forced_dt=forced_dt, t_end=None, plot_individual_plots=False, h=h, save_plots=True, 
                             r_fitrange=r_fitrange)
    Oh_f_list.append(Ohf_)
    
    D_list.append(D_)
    t_start_list.append(t_start_)
    h_list.append(h_)
    Oh_d_list.append(Ohd_.tolist())
    # break

temp_folder_names=load_folders(["/media/markEnAman/BackupNator/discoverer/water"])
# print(temp_folder_names)
folder_dict = {}
for folder in temp_folder_names:
    # if "2025_13_10_" not in folder:
    #     continue
    hf_raw = re.search(r"_hf_([^_]+)", folder).group(1)
    skip_Oh=[0.001]
    skip_Oh=[]
    # convert '0p05' to '0.05'
    hf_value = float(hf_raw.replace("p", "."))
    if hf_value not in folder_dict:
        folder_dict[hf_value] = []

    folder_dict[hf_value].append(folder)
print(folder_dict.keys())
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
    forced_dt=None
    # forced_exponent=None
    r_fitrange = [(0.16, 0.6)] +[(0.16, 0.6)] + [(0.16, 0.7)]*2 +[(0.17,0.7)]+ [(0.2, 0.7)]*5
    Ohf_, D_, t_start_, h_, Ohd_ = create_all_plots(folders, fig_save_dir="figures/water/diffOhDrop/", forced_exponent=0.5 ,
                            forced_dt=forced_dt, t_end=None, plot_individual_plots=False, h=h, save_plots=True, 
                             r_fitrange=r_fitrange)
    Oh_f_list.append(Ohf_)
    D_list.append(D_)
    t_start_list.append(t_start_)
    h_list.append(h_)
    Oh_d_list.append(Ohd_.tolist())
    # break



data = {
    "Oh_f_list": Oh_f_list,
    "D_list": D_list,
    "t_start_list": t_start_list,
    "h_list": h_list,
    "Oh_d_list": Oh_d_list
}

with open("saved_lists.json", "w") as f:
    json.dump(data, f)




plt.figure(99)
# plt.xlim(1e-1, 1.5e3)
ax = plt.gca()
leg = ax.get_legend()
if leg:
    leg.remove()
save_plot(99, "figures/water/diffOhDrop/"+"DvsOh.png")

plt.close('all')
plt.figure(1)    
handles, labels = [], []
ax = plt.gca()
# handles.append(plt.Line2D([0], [0], color="black", marker="x", linestyle="none",
# markerfacecolor='none', markeredgewidth=1))
# labels.append(r"grid refinement level 11")
handles.append(plt.Line2D([0], [0], color="blue", marker="s", linestyle="none",
markerfacecolor='blue', markeredgewidth=1))
labels.append(r"h=0.006")

handles.append(plt.Line2D([0], [0], color="green", marker="s", linestyle="none",
markerfacecolor='green', markeredgewidth=1))
labels.append(r"h=0.015")

handles.append(plt.Line2D([0], [0], color="red", marker="s", linestyle="none",
markerfacecolor='red', markeredgewidth=1))
labels.append(r"h=0.03")

handles.append(plt.Line2D([0], [0], color="yellow", marker="s", linestyle="none",
markerfacecolor='yellow', markeredgewidth=1))
labels.append(r"h=0.05")

handles.append(plt.Line2D([0], [0], color="magenta", marker="s", linestyle="none",
markerfacecolor='magenta', markeredgewidth=1))
labels.append(r"h=0.1")

handles.append(plt.Line2D([0], [0], color="black", marker="s", linestyle="none",
markerfacecolor='none', markeredgewidth=1))
labels.append(r"$Oh_d=0.001$")

handles.append(plt.Line2D([0], [0], color="black", marker="D", linestyle="none",
markerfacecolor='none', markeredgewidth=1))
labels.append(r"$Oh_d=0.0025$")

handles.append(plt.Line2D([0], [0], color="black", marker="o", linestyle="none",
markerfacecolor='none', markeredgewidth=1))
labels.append(r"$Oh_d=0.005$")

handles.append(plt.Line2D([0], [0], color="black", marker="x", linestyle="none",
markerfacecolor='none', markeredgewidth=1))
labels.append(r"$Oh_d=0.01$")

handles.append(plt.Line2D([0], [0], color="black", marker=">", linestyle="none",
markerfacecolor='none', markeredgewidth=1))
labels.append(r"Experiments (Nath & Quéré)")

handles.append(plt.Line2D([0], [0], color="black", marker="v", linestyle="none",
markerfacecolor='none', markeredgewidth=1))
labels.append("Experiments (Nath & Quéré)\nPost-processed myself")

handles.append(plt.Line2D([0], [0], color="black", linestyle="--"))
labels.append(r"$\frac{D}{D_0} \sim 1$")

# handles.append(plt.Line2D([0], [0], color="black", linestyle=":"))
# labels.append(r"$\frac{D}{D_0} \sim\left(Oh(\frac{R}{h})\right)^{-1}$")
# for i in range(len(h_list)):
#     handles.append(plt.Line2D([0], [0], color=colors[i], marker="o", linestyle="none"))
#     labels.append(f"$h = {h_list[i]}$")

ax.legend([])  # This removes the original legend
ax.legend(handles=handles, labels=labels, loc='best', fontsize=14, markerscale=1.5,)# Add the custom legend
# plt.xlim(1e-1, 1.5e3)
save_plot(1, "figures/water/diffOhDrop/"+"DvsOh_legend.png")
plt.close('all')
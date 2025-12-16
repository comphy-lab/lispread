import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.create_slip_velocity_plots import create_all_plots
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, save_plot, plot_triangle_with_labels


plt.close('all')
main_directory = "/media/markEnAman/Mark1000/discoverer"

forced_dt = None
folders = [main_directory + "/" + d for d in os.listdir(main_directory) if d[0]=="1" ] 

temp_folder_names=load_folders(folders)

folder_dict = {}
for folder in temp_folder_names:
    hf_raw = re.search(r"_hf_([^_]+)", folder).group(1)
    hf_value = float(hf_raw.replace("p", "."))
    if hf_value not in folder_dict:
        folder_dict[hf_value] = []
    folder_dict[hf_value].append(folder)
forced_dt = None
forced_dt = [
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    None,  
    0.0203, 
    0.021, 
    0.022, 
    0.023, 
    0.028, 
    0.029, 
    0.03, 
    0.032, 
    0.066, 
    0.069, 
    0.071, 
    0.075, 
    0.163, 
    0.169, 
    0.176, 
    0.183, 
    0.291, 
    0.316, 
    0.324, 
    0.342, 
     100, #0.342, 
     100, #0.584, 
    0.810, 
     100, #0.840, 
     100, #0.840, 
     100, #0.3869153736152997, 
     100, #1e-10, 
     None, 
     100, #1.7177378798291996,
     100, #0,
     100, #0,
     100]
for key in folder_dict.keys():
    h = float(key)
    print(h)
    # if h == 0.006:
    #     continue
    # Ohd_raw = re.search(r"_Ohd_([^_]+)", folder).group(1)
    
    # # convert '0p05' to '0.05'
    # Ohd_value = float(Ohd_raw.replace("p", "."))

    folders = folder_dict[key]
    print([d.split("/")[-1][:4] for d in folders])
    r_fitrange = [(0.16, 0.6)]*8 + [(0.16, 0.7)]*8 +[(0.17,0.7)]*4+ [(0.2, 0.7)]*4 + [(0.25, 0.7)]*16
    create_all_plots(folders, fig_save_dir="figures/water/diffOhDrop/", forced_exponent=0.5 ,
                            forced_dt=forced_dt, t_end=None, plot_individual_plots=False, h=h, save_plots=True, 
                             r_fitrange=r_fitrange, skip_Oh=[0.01, 0.05, 0.5, 2.5, 5, 10])
    break
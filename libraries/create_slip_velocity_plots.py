import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, remove_isolated_points
                                            
import matplotlib.patches as patches

    
def create_all_plots(folders,fig_save_dir, forced_exponent = None, forced_dt=None, t_end=None, t_plot=None, h=0.05, 
            rhof=0.9, plot_individual_plots=False, save_plots=True, linestyle="--", skip_Oh=[], marker=".", r_fitrange=None):
    """
    create and save all plots, the region means if you are in the linear or in the power 0.5 region
    """
    if t_end is None:
        t_end = np.inf + np.zeros( len(folders))
    if t_plot is None:
        t_plot = np.inf + np.zeros( len(folders))
    # preparte Oh_f values for plotting and saving
    unique_ohf = sorted({get_Ohf_from_folder_name(f) for f in folders})
    cmap = plt.get_cmap("tab10")
    ohf_to_color = {ohf: cmap(i % 10) for i, ohf in enumerate(unique_ohf)}
    

    markers = [">", "s", "D", "^", "v", "o", "<", "p", "*", "h"]

    ## lists for plotting
    i = -1
    Oh = []
    t_start = []
    D_list = []
    colors = []
    exponent_list = []

    for f in folders:
        i +=1
        # load data and Oh
        try:
            t, z, r, v, theta1, theta2 = load_data(f)
        except Exception as e: 
            print(e, ", folder=", f)
            continue
        l = get_Ohf_from_folder_name(f.split("/")[-1])
        if l in skip_Oh: 
            continue
        
        Ohd = float(re.search(r"_Ohd_([^_]+)", f.split("/")[-1]).group(1).replace("p", "."))
        Ohf = float(re.search(r"_Ohf_([^_]+)", f.split("/")[-1]).group(1).replace("p", "."))
        print(Ohd)
        # setup color and labels for plotting
        color = ohf_to_color[l]
        label = r'$Oh = $' + f'{l}'+r" $h = $" + f'{h}'

        # apply filters to data
        theta_deg = theta2 / np.pi * 180
        if r_fitrange is None:
            mask = (r > 0.2) & (t < t_end[i]) & (r < 0.7) 
        else:
            mask = (r > r_fitrange[i][0]) & (t < t_end[i]) & (r < r_fitrange[i][1])
        # mask = (r > 0.03)  & (t < t_end[i])
        # mask = (theta_deg < 160) & (t < t_end[i])
        mask = remove_isolated_points(mask)
        if len(t[mask]) ==0:
            print("no datapoints in fitrange")
            continue
        
        t_min = t[mask][0]
        t_max = t[mask][-1]
        print(t_min)
        t_o, r_o, v_o = t.copy(), r.copy(), v.copy()
        t_o, r_o, v_o, z,  theta1_o, theta2_o  = t_o[t_o<t_plot[i]], r_o[t_o<t_plot[i]], v_o[t_o<t_plot[i]], z[t_o<t_plot[i]], theta1[t_o<t_plot[i]],  theta2[t_o<t_plot[i]]
        t, r, v, theta1, theta2 = t[mask], r[mask], v[mask], theta1[mask], theta2[mask]
        sigma = 5
        if l > 1:
            sigma=10
        # if l <20:
        #     forced_dt = 0.239*l**0.793
        # fit data
        bb = None
        if forced_dt is not None:
            bb = forced_dt[i]
        if bb is not None and bb >=10:
            print(f"for Ohf={l}: to high dt forced")
            continue
        v_smooth = gaussian_filter1d(v_o, sigma=sigma)
        _, v_s = log_sampler(t, v, 50)
        t_s, r_s = log_sampler(t, r, 50)
        a, b, c, pcov = get_fit(t_s, r_s, cc=forced_exponent, bb=bb)
        if c > 1.99: #or l>4.9: 
            print(f"for Ohf={l}: no fit found or skipped")
            continue
        print(f"Fit parameters for Ohf={l}: a={np.round(a, 2)}, dt={np.round(b, 2)}, c={np.round(c, 2)}")
        dt = b
        print(dt)
        D = (a**2)/2
        D_list += [D]
        Oh.append(l)
        t_start.append(b)
        exponent_list.append(c)
        R = 1
        create_plot(Ohf*R/h/(1+Ohf*Ohd*R/h), D, 2, fmt =".", xlabel="Ohd", ylabel = "D", xscale="log", yscale="log")
        create_plot(Ohd, D, 1, fmt =".", xlabel="Ohd", ylabel = "D", xscale="log", yscale="log")
    save_plot(2, fig_save_dir+ "DvsOhdwith.png", dpi=300)
    save_plot(1, fig_save_dir+ "DvsOhd.png", dpi=300)

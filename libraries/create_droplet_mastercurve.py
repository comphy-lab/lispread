import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, remove_isolated_points
                                            
import matplotlib.patches as patches
def mastercurve(t, rc, t0, tauc):
    tau = t - t0
    if np.any(tau <= 0):
        assert False
    return (2 * rc) * (1 / (tau / tauc) + 1/np.sqrt(tau / tauc))**-1

def get_fit(x, y, bb=None, aa=None, cc=None):

    lower_bounds = [0.01, 0 ,0.01]  # no lower restriction
    upper_bounds = [100, np.min(x), 1000]     # no upper restriction

    
    if aa is not None:
        lower_bounds[0] = aa - 1e-6
        upper_bounds[0] = aa + 1e-6
    if bb is not None:
        lower_bounds[1] = bb - 1e-6
        upper_bounds[1] = bb + 1e-6
    if cc is not None:
        lower_bounds[2] = cc - 1e-6
        upper_bounds[2] = cc + 1e-6
        


    bounds = (lower_bounds, upper_bounds)
    # Fit the function to the data
    popt, pcov = curve_fit(mastercurve, x, y, bounds=bounds, maxfev=20000)
    rc, t0, tauc = popt
    return rc, t0, tauc, pcov
    

def create_mastercurve_plots(folders,fig_save_dir, forced_exponent = None, forced_dt=None, rc=None, tauc=None, t_end=None, t_plot=None, h=0.05, 
            rhof=0.9, plot_individual_plots=False, save_plots=True, linestyle="--", skip_Oh=[], marker="."):
    """
    create and save all plots, the region means if you are in the linear or in the power 0.5 region
    """
    if t_end is None:
        t_end = np.inf + np.zeros( len(folders))
    if t_plot is None:
        t_plot = np.inf + np.zeros( len(folders))
    if rc is None:
        rc = 1+ np.zeros( len(folders))
    if tauc is None:
        tauc = 1+ np.zeros( len(folders))
    # preparte Oh_f values for plotting and saving
    unique_ohf = sorted({get_Ohf_from_folder_name(f) for f in folders})
    cmap = plt.get_cmap("tab10")
    ohf_to_color = {ohf: cmap(i % 10) for i, ohf in enumerate(unique_ohf)}
    ## lists for plotting
    i = -1
    Oh = []
    t_start = []
    D_list = []
    colors = []
    exponent_list = []

    for f in folders:
        i +=1
        print(i)
        try:
            # load data and Oh
            t, z, r, v, theta1, theta2 = load_data(f)
            l = get_Ohf_from_folder_name(f.split("/")[-1])
            if l in skip_Oh: 
                continue

            # setup color and labels for plotting
            color = ohf_to_color[l]
            label = r'$Oh = $' + f'{l}'+r" $h = $" + f'{h}'

            # apply filters to data
            theta_deg = theta2/np.pi * 180
            mask = (r>0.05) & (t < t_end[i]) & (r < 0.9) 
            # mask = (r > 0.03)  & (t < t_end[i])
            # mask = (theta_deg < 160) & (t < t_end[i])
            mask = remove_isolated_points(mask)
            if len(t[mask]) ==0:
                continue
            
            t_min = t[mask][0]
            t_max = t[mask][-1]
            t_o, r_o, v_o = t.copy(), r.copy(), v.copy()
            t_o, r_o, v_o, z,  theta1_o, theta2_o  = t_o[t_o<t_plot[i]], r_o[t_o<t_plot[i]], v_o[t_o<t_plot[i]], z[t_o<t_plot[i]], theta1[t_o<t_plot[i]],  theta2[t_o<t_plot[i]]
            t, r, v, theta1, theta2 = t[mask], r[mask], v[mask], theta1[mask], theta2[mask]
            if forced_dt is not None:
                dt = forced_dt[i]
            else:
                dt = None
            # rc = float(l)
            # rc = float(l)
            # rc = 1
            # tauc = np.sqrt(float(l)) 
            # tauc  = float(l) **2
            # tauc *= 1/0.0021
            # print(tauc)
            # rc, dt, tauc, popt = get_fit(t, r, bb=dt)
            # print( rc, dt, tauc)
            # # plot r vs t
            # print(dt)
            # # dt = 0
            # # rc = float(l)
            # # rc = float(l) 
            # # rc = 1
            # # tauc = np.sqrt(float(l)) 
            # # tauc  = float(l) **2
            # # tauc *= 0.0021
            # create_plot((t-dt)/tauc,  (r)/rc, 1, color=color, label=label, alpha=0.7, 
            #             xlabel=r'$\tau/\tau_c$', ylabel=r'$r/r_c$', title=None, xscale="log", yscale="log")
            # create_plot((t-dt)/tauc,  mastercurve(t-dt, rc, 0, tauc)/rc, 1, color="k", label="fit", alpha=0.7, 
            #             xlabel=r'$\tau/\tau_c$', ylabel=r'$r/r_c$', title=None, xscale="log", yscale="log")
            # plt.xlim(1e-2, 100)
            # plt.ylim(1e-2, 100)
            create_plot((t-dt),  (r), 2, color=color, label=label, alpha=0.7, 
                        xlabel=r'$\tau/\tau_c$', ylabel=r'$r/r_c$', title=None, xscale="log", yscale="log")
            # plt.xlim(1e-2, 100)
            # plt.ylim(1e-2, 100)
            create_plot([1e-1, 1], [1e-1, 1], 2, fmt="k--", alpha=0.5)
        except Exception as e:
            print(e)
    if save_plots:
        # r vs t
        save_plot(2, fig_save_dir + "rvstmindt.png")
        save_plot(1, fig_save_dir + "rrc_vs_tautauc_cropped.png")
        
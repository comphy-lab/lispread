import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend, remove_isolated_points, ELS_func, fit_ELS_law
                                            
import matplotlib.patches as patches

                                            
    
def create_glycerol_plots(folders,fig_save_dir, forced_dt=None, t_end=None, h=0.05, 
            rhof=0.9, plot_individual_plots=False, save_plots=True, linestyle="--", skip_Oh=[], marker="."):
    """
    create and save all plots, the region means if you are in the linear or in the power 0.5 region
    """
    if t_end is None:
        t_end = np.inf + np.zeros( len(folders))
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
        mask = (r>0.2) & (t < t_end[i])
        mask = remove_isolated_points(mask)
        if len(t[mask]) ==0:
            continue
        
        t_min = t[mask][0]
        t_max = t[mask][-1]
        t_o, r_o, v_o = t.copy(), r.copy(), v.copy()
        t_o, r_o, v_o, z,  theta1_o, theta2_o  = t_o[t_o<t_end[i]], r_o[t_o<t_end[i]], v_o[t_o<t_end[i]], z[t_o<t_end[i]], theta1[t_o<t_end[i]],  theta2[t_o<t_end[i]]
        t, r, v, theta1, theta2 = t[mask], r[mask], v[mask], theta1[mask], theta2[mask]
        sigma = 5
        if l > 1:
            sigma=10
        v_smooth = gaussian_filter1d(v_o, sigma=sigma)
        dt = None
        print(forced_dt)
        if forced_dt is not None:
            dt = forced_dt[i]
        print(dt)
        t_s, r_s = log_sampler(t, r, 50)
        tau, t0, pcov = fit_ELS_law(t_s, r_s, dt)
        print(t0)
        Oh.append(l)
        t_start.append(t0)
        dt = t0
        
        # plot r vs t
        create_plot(t_o,  r_o, 2, fmt=linestyle, color=color, label=label, alpha=0.7, 
                    xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)
                    
        create_plot(t_o-dt, r_o/np.log(1/r_o), 3, fmt=linestyle, label=label, xlabel=r'$\tilde t-dt$', ylabel=r'$\frac{\tilde{r}}{\ln(1/\tilde{r})}$', 
                    title=None, alpha=0.7, color=color)
        plt.xlim(1e-3, 10)

        create_plot((t_o)-dt, r_o/np.log(1/r_o), 444, fmt=".", color=color, label=label, xlabel=r'$\tilde t - \tilde t_0$', ylabel=r'$\frac{\tilde{r}}{\ln(1/\tilde{r})}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2)
        plt.xlim(1e-3, 10)
        create_plot((r/1000/ np.log(1/r))*tau*3000, r/np.log(1/r), 444, fmt="--k", label="ELS fit", alpha=0.8)
        

        # plot TP velocity vs time
        create_plot(t_o, v_smooth, 10, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$', title=None, alpha=1, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t_o, v_o, 11, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$)', title=None, alpha=1,markersize=0.7, xscale="log", yscale="log")
        plt.xlim(1e-3, 10)
        
    if save_plots:
        save_plot(2, fig_save_dir+'r_vs_t.png')
        save_plot(3, fig_save_dir+'r_vs_tlog.png')
        save_plot(10, fig_save_dir+'v_vs_t_smooth_all.png')
        save_plot(11, fig_save_dir+'v_vs_t_all.png')
        save_plot(444, fig_save_dir+'r_vs_t_shifted_loglog_all.png')

        
    create_plot(Oh, np.array(t_start), 111, fmt=".", xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$t_0$")
    if save_plots:
        save_plot(111, fig_save_dir+'t_startvsOH.png')
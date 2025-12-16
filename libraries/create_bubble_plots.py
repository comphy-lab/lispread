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

                                            
    
def create_bubble_plots(folders,fig_save_dir, forced_exponent = None, forced_dt=None, t_end=None, t_plot=None, h=0.05, 
            rhof=0.9, plot_individual_plots=False, save_plots=True, linestyle="--", skip_Oh=[], marker="."):
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
    
    ## lists for plotting
    i = -1
    Oh = []
    t_start = []
    D_list = []
    colors = []
    exponent_list = []

    for f in folders:
        i +=1
        try:
            print(i)
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
            mask = (r>0.2) & (t < t_end[i]) & (r < 0.9) 
            # mask = (r > 0.03)  & (t < t_end[i])
            # mask = (theta_deg < 160) & (t < t_end[i])
            mask = remove_isolated_points(mask)
            if len(t[mask]) ==0:
                continue
            
            t_min = t[mask][0]
            t_max = t[mask][-1]
            print(t_end[i])
            t_o, r_o, v_o = t.copy(), r.copy(), v.copy()
            t_o, r_o, v_o, z,  theta1_o, theta2_o  = t_o[t_o<t_plot[i]], r_o[t_o<t_plot[i]], v_o[t_o<t_plot[i]], z[t_o<t_plot[i]], theta1[t_o<t_plot[i]],  theta2[t_o<t_plot[i]]
            t, r, v, theta1, theta2 = t[mask], r[mask], v[mask], theta1[mask], theta2[mask]
            sigma = 5
            if l > 1:
                sigma=10
            v_smooth = gaussian_filter1d(v_o, sigma=sigma)
            _, v_s = log_sampler(t, v, 50)
            t_s, r_s = log_sampler(t, r, 50)
            # fit data
            a, b, c, pcov = get_fit(t, r, cc=forced_exponent, bb=forced_dt[i], N=10)
            
            if c > 1.99: #or l>4.9: 
                print(f"for Ohf={l}: no fit found or skipped")
                continue
            print(f"Fit parameters for Ohf={l}: a={np.round(a, 2)}, dt={np.round(b, 2)}, c={np.round(c, 2)}")
            dt = b
            print(dt)
            D = a**2/2
            # D = a
            D_list += [D]
            Oh.append(l)
            t_start.append(b)
            exponent_list.append(c)


            # plot r vs t
            create_plot(t,  r, 1, color=color, label=label, alpha=0.7, 
                        xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)
            create_plot(t_o,  r_o, 2, color=color, label=label, alpha=0.7, 
                        xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)

            create_plot(t_o,  r_o, 3, color=color, label=label, alpha=0.7, xscale='log', yscale='log',
                        xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)
            create_plot(t_o-dt,  r_o, 4, fmt = ".",color=color, label=label, alpha=0.7, xscale='log', yscale='log',
                        xlabel=r'$\tilde t -t_0$', ylabel=r'$\tilde{r}$', title=None, markersize=2)
                        
            plt.xlim(1e-3, 5)

            plt.ylim(0.08, 2)
            create_plot((t_o-dt)*2*D,  r_o, 5, fmt = ".",color=color, label=label, alpha=0.7, xscale='log', yscale='log',
                        xlabel=r'$2D(\tilde t -\tilde t_0)$', ylabel=r'$\tilde{r}$', title=None, markersize=2)
           
            plt.xlim(1e-3, 5)

            plt.ylim(0.08, 2)

            # plot theta 
            create_plot(t_o, theta2_o / np.pi * 180, 555, xlabel=r'$\tilde t$', ylabel=r'$\theta$', fmt=linestyle, label=label, alpha=0.7, xscale="log", yscale="log", color=color)
            create_plot(t_o * 0 + t_min, theta2_o / np.pi * 180, 555, fmt="-", color=color, xscale="log", yscale="log")
            create_plot(t_o * 0 + t_max, theta2_o / np.pi * 180, 555, fmt="-", color=color, xscale="log", yscale="log")
            create_plot(t, theta2 / np.pi * 180, 556, xlabel=r'$\tilde t$', ylabel=r'$\theta$', fmt=linestyle, label=label, alpha=0.7, xscale="log", color=color)
        
        except Exception as e:
            print(f"Could not process folder {f} due to error: {e}")
            continue
    Oh = np.array(Oh)
    create_plot(Oh, np.array(D_list), 99, label ="h="+str(h), alpha = 0.6,  # 0.9 therm to account for difference paper D0 and our D0 in surface tension
                    fmt=marker, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", 
                    ylabel = r"$D/D_0$", markerfacecolor='none', markeredgewidth=1,markersize=20)
    create_plot([6666, 6666], [5e-2, 2], 99, fmt="r--", label="highest Oh(R/h) simulation")
    if save_plots:
        # r vs t
        save_plot(1, fig_save_dir + "r_vs_t_cropped.png")
        save_plot(2, fig_save_dir + "r_vs_t.png")
        save_plot(3, fig_save_dir + "logr_vs_logt.png")
        save_plot(4, fig_save_dir + "logr_vs_logtmint0.png")
        save_plot(5, fig_save_dir + "logr_vs_logtmint0alpha.png")

        # theta
        save_plot(555, fig_save_dir+'thetavst_originol.png', dpi=300)
        save_plot(556, fig_save_dir+'thetavst.png', dpi=300)

        # D vs Oh
        data_alex = np.array([[0.00003593813663804633, 1.4862372525714524],
            [0.004691333380048315, 1.3428168711541681],
            [0.050547968211912354, 1.2519488014546076],
            [0.4792427543884916, 0.9056866460786612],
            [4.741611045635237, 0.451621279304005],
            [46.913333800483045, 0.3322852150173862],
            [533.1529933327472, 0.38598349151390027],
            [4691.333380048324, 0.36073462331628653]])
        R = 1
        h = 0.05
        create_plot(data_alex[:,0], (data_alex[:,1])**2/2 *(1-np.cos(110/180*np.pi))**(1/4), 99, label ="(Oratis, unpublished)", alpha = 0.75,  
                    fmt=">k" , markeredgewidth=1, markerfacecolor='none')
        # create_plot(data_alex[:,0] * 1/np.sqrt(R), (data_alex[:,1])**2/2, 99, label ="Alex data", alpha = 0.75,  
        #             fmt="ks" , markeredgewidth=1, markerfacecolor='none')
        save_plot(99, fig_save_dir + "DvsOh.png")
        print(t_start)
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
        v_smooth = gaussian_filter1d(v_o, sigma=sigma)
        _, v_s = log_sampler(t, v, 50)
        t_s, r_s = log_sampler(t, r, 50)
        # if l <20:
        #     forced_dt = 0.239*l**0.793
        # fit data
        bb = None
        if forced_dt is not None:
            bb = forced_dt[i]
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
        # plot contact angle
        create_plot(t_o, theta2_o / np.pi * 180, 555, xlabel=r'$\tilde t$', ylabel=r'$\theta$', fmt=linestyle, label=label, alpha=0.7, xscale="log", yscale="log", color=color)
        create_plot(t_o * 0 + t_min, theta2_o / np.pi * 180, 555, fmt="-", color=color, xscale="log", yscale="log")
        create_plot(t_o * 0 + t_max, theta2_o / np.pi * 180, 555, fmt="-", color=color, xscale="log", yscale="log")
        create_plot(t, theta2 / np.pi * 180, 556, xlabel=r'$\tilde t$', ylabel=r'$\theta$', fmt=linestyle, label=label, alpha=0.7, xscale="log", color=color)
        
        
        # plot r vs t
        create_plot(t_o,  r_o, 2, fmt=linestyle, color=color, label=label, alpha=0.7, 
                    xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)
        create_plot(t_o, r_o, 3, fmt=linestyle, label=label, xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', 
                    title=None, alpha=0.7, color=color, xscale="log", yscale="log")
        create_plot([np.min(t_o), np.max(t_o)], [1.5e-1*np.sqrt(0.03)]*2, 3, fmt="-", color="k", xscale="log", yscale="log")
        create_plot([np.min(t_o), np.max(t_o)], [1.5*np.sqrt(0.03)]*2, 3, fmt="-", color="k", xscale="log", yscale="log")
        create_plot([np.min(t_o), np.max(t_o)], [2*np.sqrt(0.03)]*2, 3, fmt="-", color="k", xscale="log", yscale="log")

        if r_fitrange is not None:
            r_min = r_fitrange[i][0]
        else:
            r_min = 0.2
        create_plot((t_o-dt)[(r_o>r_min)][::-1], r_o[(r_o>r_min)][::-1], 444, fmt=".", color=color, label=label, xlabel=r'$\tilde t - \tilde t_0$', ylabel=r'${\tilde{r}}$', 
                    title=None, alpha=1, xscale="log", yscale="log",markersize=5)  #markersize=6, markerfacecolor='white', markeredgewidth=2)
        create_plot((t_o-dt)[(r_o>r_min)], func(t_o-dt, a, 0, c)[(r_o>r_min)], 444, fmt="--", color="k", alpha=0.7)
        plt.ylim(1.9e-1, 2 )
        create_plot((t_o-dt)[(r_o>r_min)]*2*D, r_o[(r_o>r_min)], 5, fmt=".", color=color, label=label, xlabel=r'$(\tilde t - \tilde t_0) 2D$', ylabel=r'${\tilde{r}}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2)
        plt.xlim(1e-2, 2)
        
        create_plot((t), r, 445, fmt=".", color=color, label=label, xlabel=r'$\tilde t$', ylabel=r'${\tilde{r}}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2)
        create_plot(t_o*0.5, r_o * 650, 124, fmt=linestyle, label=label, xlabel=r'$t(ms)$', ylabel=r'$r(\mu m)$', 
                    title=None, alpha=0.7, color=color, xscale="log", yscale="log")
        plt.ylim(10,1000)

        # plot r vs t log and corrected
        # create_plot(t_o*l**-0.8, r_o, 4, fmt=linestyle, color=color, label=label, xlabel=r'$\tilde t \cdot Oh^{0.8}$', ylabel=r'${\tilde{r}}$', 
        #             title=None, alpha=0.7, xscale="log", yscale="log")
        # plot r vs t log and corrected
        # create_plot((t_o-dt)*D, r_o, 5, fmt=".", color=color, label=label, xlabel=r'$(\tilde t-t_0) \tilde D$', ylabel=r'${\tilde{r}}$', 
        #         title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2)

        # plot TP velocity vs time
        create_plot(t, v/a , 9, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$2\tilde v(\tilde t)/{a}$', title=None, alpha=1, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t_o, v_smooth, 10, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$', title=None, alpha=1, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t_o, v_o, 11, color=color, label=label, xlabel=r'$\tilde t$',  fmt = ".",
                    ylabel=r'$\tilde v(\tilde t)$)', title=None, alpha=1,markersize=2, xscale="log", yscale="log")
        create_plot([dt, dt], [1e-3, 10], 11, color=color, fmt = "--",xscale="log", yscale="log")
        plt.xlim(1e-3, 10)
        
        create_plot(t_o, z, 101, color=color, fmt = ".", xlabel="t", ylabel="z",xscale="log", yscale="log",  markersize=2)
        create_plot([dt, dt], [1e-3, 1], 101, color=color, fmt = "--", xlabel="t", ylabel="z",xscale="log", yscale="log")
        # plot individual plots
        if plot_individual_plots:
            # plot single plots, corrected data r vst t and v vs t
            temp = np.linspace(min(t), max(t), 100)
            create_plot(t_o - dt, r_o/np.sqrt(h), 7, fmt='.', color=color, label=label, xlabel=r'$\tilde t - \tilde t_0$', ylabel=r'${{r}}/\sqrt{hR}$', 
                        title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2, subplot=121)
            create_plot(temp, func(temp, a/np.sqrt(h), 0, c), 7, fmt='k--', label=r"fitted, $n=$" + str(np.round(c,2)), 
                        alpha=0.7,  markersize=2, subplot=121)
            save_plot(7, fig_save_dir+'corrected_single_plots/rvst_corrected_log_'+str(l)+".png" , dpi=300)
            plt.clf()

            
            # plot single plots, uncorrected data
            temp = np.linspace(min(t), max(t), 100)
            create_plot(t_o, r_o, 77, fmt='.', color=color, label=label, xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$)', 
                        title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2, subplot=121)
            create_plot(temp, temp**0.5, 77, fmt="k--", label = r"$\sim t^{0.5}$",subplot=121)
            create_plot(temp, temp**0.4, 77, fmt="k--", alpha=0.25, label = r"$\sim t^{0.4}$", subplot=121)
            create_plot(temp, temp, 77, fmt="r--", alpha=1, label = r"$\sim t^{1}$", subplot=121)
            create_plot(temp, temp**-0.5/3, 77, fmt="k--", label = r"$\sim t^{-0.5}$", subplot=122)
            create_plot(temp, temp**-0.67/3, 77, fmt="k--", alpha=0.25, label = r"$\sim t^{-0.67}$", subplot=122)
            create_plot(t_o, v_o, 77, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$', title=None, alpha=0.5, xscale="log", yscale="log",  markersize=0.7, subplot=122)

            save_plot(77, fig_save_dir+'uncorrected_single_plots/rvst_uncorrected_log_'+str(l)+".png" , dpi=300)
            plt.clf()
            
    if save_plots:
        temp = np.linspace(1e-1, 20, 10000)
        save_plot(555, fig_save_dir+'thetavst_originol.png', dpi=300)
        save_plot(556, fig_save_dir+'thetavst.png', dpi=300)
        save_plot(2, fig_save_dir+'rvst_originol.png', dpi=300)
        create_plot(temp, temp**0.4, 4, alpha = 0.8, fmt="k:", label = r"$r\sim t^{0.4}$")
        create_plot(temp, temp**0.5, 4, alpha = 0.8, fmt="k--", label = r"$r\sim t^{0.5}$")
        # create_plot(temp, temp**0.5, 444, alpha = 0.1, fmt="k--", label = r"$r\sim t^{0.5}$")
        # plt.xlim(0.4, 10)
        # plt.ylim(0.4, 4)
    
        save_plot(444, fig_save_dir+'rvst_collapsed.png', dpi=300)
        save_plot(445, fig_save_dir+'rvst.png', dpi=300)
        save_plot(124, fig_save_dir+'tmsvsrmum.png', dpi=300)
        save_plot(3, fig_save_dir+'rvst_originol_log.png', dpi=300)
        temp = np.linspace(1e-1, 3, 100)
        # create_plot(temp, temp**1, 4, fmt="k--", alpha=1, label = r"$\sim t^{1}$")
        save_plot(4, fig_save_dir+'rvst_corrected_log.png', dpi=300)
        save_plot(88, fig_save_dir+'rvst_corrected_log.png', dpi=300)
        save_plot(5, fig_save_dir+'rvstD_corrected_log.png', dpi=300)
        save_plot(101, fig_save_dir+'zvst.png', dpi=300)

        save_plot(9, fig_save_dir + 'vvst_corrected.png', dpi=300)
        save_plot(10, fig_save_dir + 'vvst_filtered.png', dpi=300)
        save_plot(11, fig_save_dir + 'vvst_original.png', dpi=300)

    # plot D vs Oh
    Oh_asymptotes = np.linspace(1e-4, 1e5, 10000)
    alpha = 2.8**2
    beta = np.sqrt(0.15)
    R = 1
    create_plot((np.array(Oh) * (R/h)), np.array(D_list), 99, label ="h="+str(h), alpha = 0.6,  # 0.9 therm to account for difference paper D0 and our D0 in surface tension
                fmt=marker, xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", 
                ylabel = r"$D/D_0$", markerfacecolor='none', markeredgewidth=1)
    # x_min, x_max = 0.1, 1e3
    # y_min, y_max = 0.05, 0.5
    # plt.xlim(1e-2, 1000)
    # plt.ylim(0.05, 0.5)
    # plt.xlim(x_min, x_max)
    # plt.ylim(y_min, y_max)
    # Create a rectangle patch
    # box = patches.Rectangle(
    #     (x_min, y_min),           # bottom-left corner (x, y)
    #     x_max - x_min,            # width
    #     y_max - y_min,            # height
    #     linewidth=2,              # border thickness
    #     edgecolor='red',          # box color
    #     facecolor='none'          # transparent fill
    # )
    # plt.gca().add_patch(box)
    asymptote_low = 1/np.sqrt(alpha) * np.ones(len(Oh_asymptotes)) *1.41* np.sqrt(0.7/0.6) 
    # asymptote_high = 1 / (2*beta * Oh_asymptotes * R/h)
    # crit = (asymptote_high<asymptote_low)
    # create_plot(Oh_asymptotes[crit]*R/h, asymptote_high[crit], 99, fmt = ":"+marker[-1])
    # create_plot(Oh_asymptotes[~crit]*R/h, asymptote_low[~crit], 99, fmt = "k--", label=r"$\frac{D}{D_0} \sim \frac{1}{\alpha}$")
    # plt.ylim(1e-2, 0.4)
    #ylabel = r"$D/D_0\cdot \frac{\sqrt{\gamma_{1}+\gamma_2}}{\sqrt{\gamma_{drop}}}$", markerfacecolor='none', markeredgewidth=1)
    
    if save_plots:
        data_Nath = np.array([[0.7790891638841551, 0.32696037174989717],
                            [0.9743726050130228, 0.32490425012906454],
                            [1.6376600853049355, 0.29186367729350216],
                            [1.9837403275323662, 0.31680825425428255],
                            [1.9837403275323673, 0.3276486331110457],
                            [3.3341376156260716, 0.2798434909337653],
                            [4.038727758592535, 0.29125058609914406],
                            [5.973596809058105, 0.22820793172418924],
                            [7.411474124471075, 0.22772855630234792],
                            [10.12054303946523, 0.18688426810555975],
                            [9.724286873438992, 0.179564775088414],
                            [19.956608162732508, 0.13321121228113264],
                            [16.47500944180125, 0.1123487326832662],
                            [80.11787126644383, 0.11570538346131634],
                            [103.4532516821998, 0.12533049713067887],
                            [157.98371267844058, 0.10749545335734109],
                            [231.81120894905442, 0.09595663884675523],
                            [202.37546008116516, 0.08529694459231732]]) \
                            * np.sqrt(0.72/0.6)     # account for different normalization of surface tension in Nath &quere paper


        
        create_plot(data_Nath[:,0], data_Nath[:,1], 99, label ="Nath & Queré", alpha = 0.75,  
                    fmt="ks", xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", 
                    ylabel = r"$D/D_0$", markeredgewidth=1, markerfacecolor='none')
        OHRh_Nath_self = np.array([145.72436405, 72.86218203, 14.4222051, 7.21110255, 2.85439476, 0.75115652])
        D_Nath_self =  np.array([0.10075624, 0.1222998,  0.19366557, 0.27575631, 0.31608867, 0.36738312])

        create_plot(OHRh_Nath_self* np.sqrt(0.7/0.6) , D_Nath_self* np.sqrt(0.72/0.6) , 99, label ="Nath & Queré \n processed myself", alpha = 0.75,  
                    fmt="kv", xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", 
                    ylabel = r"$D/D_0$", markeredgewidth=1, markerfacecolor='none')
        
        # asymptote_low = 1/np.sqrt(alpha) * np.ones(len(Oh_asymptotes)) 
        # asymptote_high = 1 / ( beta *Oh_asymptotes * R/h)
        # crit = (asymptote_high<asymptote_low)
        # create_plot(Oh_asymptotes[crit] * R/h * np.sqrt(0.7/0.6), asymptote_high[crit], 99, fmt = "k:", label=r"$\frac{D}{D_0} \sim\left(Oh(\frac{R}{h})\right)^{-1}$")
        create_plot(Oh_asymptotes* R/h, asymptote_low, 99, fmt = "k--", label=r"$\frac{D}{D_0} \sim \frac{1}{\alpha}$")
        # plot o.5 asymptote
        # asymptote_high = 1 / ( beta * np.sqrt(Oh_asymptotes) * R/h)
        # create_plot(Oh_asymptotes[crit]*R/h, asymptote_high[crit], 99, fmt = "k--", label=r"$\frac{D}{D_0} \sim\left(Oh(\frac{R}{h})\right)^{-1}$")
        
        save_plot(99, fig_save_dir+'DvsOh.png', dpi=300)



        
    create_plot(Oh, np.array(t_start), 111, fmt=".", xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$t_0$")
    create_plot(np.array(Oh), np.array(exponent_list), 63, alpha=0.6,
        fmt=marker, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$n$", label="h = "+str(h)
        , markerfacecolor='none', markeredgewidth=1)
    if save_plots:
        save_plot(111, fig_save_dir+'t_startvsOH.png')
        save_plot(63, fig_save_dir+'exponentvsOH.png')
        print(t_start)
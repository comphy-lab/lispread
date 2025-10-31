import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
from libraries.plot_contact_line_lib import load_data, load_folders, get_Ohf_from_folder_name, create_plot, \
                                            log_sampler, get_fit, func, get_lin_fit, get_D0, save_plot, kalman_1d_velocity, \
                                            make_Oh_h_legend

                                            
def get_theoretical_D(Oh, R=1, h=0.031, alpha=2.8, beta=0.15):
    # return abs(- beta * Oh * R/h + np.sqrt((beta * Oh * R/h)**2 + 4 * alpha))/(2*alpha)
    psi = Oh * R/h
    A = alpha**2
    B = beta * psi
    C = -1
    disc = B**2 - 4 * A * C
    x = abs(-B + np.sqrt(disc)) / (2.0 * A)
    return (x)
    
def create_all_plots_linear(folders,fig_save_dir, forced_exponent = None, forced_dt=None, t_end=None, 
                            h=0.05, plot_individual_plots=False, save_plots=True, linestyle="--", skip_Oh=[]):
    if t_end is None:
        t_end = np.inf + np.zeros( len(folders))
    # preparte Oh_f values for plotting and saving
    unique_ohf = sorted({get_Ohf_from_folder_name(f) for f in folders})
    cmap = plt.get_cmap("tab10")
    ohf_to_color = {ohf: cmap(i % 10) for i, ohf in enumerate(unique_ohf)}
    Oh = []

    i = -1
    t_start = []
    D_list = []
    colors = []
    exponent_list = []
    for f in folders:
        i +=1
        # load data and Oh
        t, z, r, v = load_data(f)
        l = get_Ohf_from_folder_name(f.split("/")[-1])
        if l in skip_Oh:
            continue
        # setup color and labels for plotting
        color = ohf_to_color[l]
        label = r'$Oh = $' + f'{l}'

        # apply filters to data
        mask = (r/np.sqrt(h)>1e-1) & (r/np.sqrt(h)<1)
        t_min = t[mask][0]
        t_o, r_o, v_o = t.copy(), r.copy(), v.copy()
        t, r, v = t[mask], r[mask], v[mask]
        t_o, r_o, v_o, z = t_o[t_o<t_end[i]], r_o[t_o<t_end[i]], v_o[t_o<t_end[i]], z[t_o<t_end[i]]
        sigma = 5
        if l > 1:
            sigma=10
        v_smooth = gaussian_filter1d(v_o, sigma=sigma)
        _, v_s = log_sampler(t, v, 50)
        t_s, r_s = log_sampler(t, r, 50)

        # fit data


        a, b, c, pcov = get_fit(t, r, cc=forced_exponent, bb=forced_dt)
        # a, b = get_lin_fit(t, r, bb=forced_dt)
        # c, pcov = 1, None
        if c > 1.99: #or l>4.9: 
            print(f"for Ohf={l}: no fit found or skipped")
            continue
        print(f"Fit parameters for Ohf={l}: a={np.round(a, 2)}, dt={np.round(b, 2)}, c={np.round(c, 2)}")
        dt = b
        D = a
        D_list += [D]
        Oh.append(l)
        t_start.append(b)
        exponent_list.append(c)
        # if i<3:
        #     continue
        # plot r vs t
        create_plot(t_o,  r_o, 2, fmt=linestyle, color=color, label=label, alpha=0.7, 
                    xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)
        # plt.xlim(0, 5)
        
        # plot r vs t 
        create_plot(t_o, r_o, 3, fmt=linestyle, label=label, xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', 
                    title=None, alpha=0.7, color=color, xscale="log", yscale="log")

        # plot r vs t log and corrected
        create_plot(t_o*l**-0.8, gaussian_filter1d(r_o,sigma=sigma/5), 4, fmt=linestyle, color=color, label=label, xlabel=r'$\tilde t \cdot Oh^{0.8}$', ylabel=r'${\tilde{r}}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log")
        # plot r vs t log and corrected
        create_plot((t_o-dt)*D, gaussian_filter1d(r_o,sigma=sigma/5), 5, fmt=linestyle, color=color, label=label, xlabel=r'$(\tilde t-t_0) \tilde D$', ylabel=r'${\tilde{r}}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log")

        # plot TP velocity vs time
        create_plot(t, v/a , 9, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$2\tilde v(\tilde t)/{a}$', title=None, alpha=1, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t_o, v_smooth, 10, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$', title=None, alpha=1, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t_o, v_o, 11, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$)', title=None, alpha=1,markersize=0.7, xscale="log", yscale="log")
        plt.xlim(1e-3, 10)
        # plt.ylim(1e-2, 3)
        create_plot(t_o, z, 101, xlabel="t", ylabel="z",xscale="log", yscale="log")
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
        save_plot(2, fig_save_dir+'rvst_originol.png', dpi=300)
        # create_plot(temp, temp**0.5, 3, fmt="k--", alpha=0.5, label = r"$\sim t^{0.5}}$")
        # create_plot(temp, temp, 3, fmt="k--", alpha=0.75, label = r"$\sim t$")
        save_plot(3, fig_save_dir+'rvst_originol_log.png', dpi=300)
        temp = np.linspace(1e-1, 3, 100)
        # create_plot(temp, temp**1, 4, fmt="k--", alpha=1, label = r"$\sim t^{1}$")
        save_plot(4, fig_save_dir+'rvst_corrected_log.png', dpi=300)
        save_plot(5, fig_save_dir+'rvstD_corrected_log.png', dpi=300)
        save_plot(101, fig_save_dir+'zvst.png', dpi=300)

        save_plot(9, fig_save_dir + 'vvst_corrected.png', dpi=300)
        save_plot(10, fig_save_dir + 'vvst_filtered.png', dpi=300)
        save_plot(11, fig_save_dir + 'vvst_original.png', dpi=300)

        # plot D vs Oh
    create_plot(np.array(Oh), np.array(D_list), 99, fmt=".", xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$V$", label="h = "+str(h))
    
    if save_plots:
        Oh_asymptotes = np.linspace(min(Oh), max(Oh), 10000)
        asymptote_low = np.sqrt(1/(h)) * np.ones(len(Oh_asymptotes))
        asymptote_high = (Oh_asymptotes**-(3/4) )
        crit = (asymptote_high <=asymptote_low) 
        create_plot(Oh_asymptotes[crit], asymptote_high[crit], 99, fmt = "k--", label=r"$V = Oh^{-3/4}$")
        asymptote_high = (Oh_asymptotes**-(1) )
        create_plot(Oh_asymptotes[crit], asymptote_high[crit], 99, fmt = "k-.", label=r"$V = Oh^{-1}$")
        create_plot(Oh_asymptotes[~crit], asymptote_low[~crit], 99, fmt = "k:", label=r"$V = \sqrt{\gamma /(\rho h)})$")
        save_plot(99, fig_save_dir+'DvsOh.png', dpi=300)
    create_plot(Oh, np.array(t_start)+1, 111, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$t_0$")
    create_plot(np.array(Oh), np.array(exponent_list), 63, fmt=".", xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$c$", label="h = "+str(h))
    
    if save_plots:
        save_plot(111, fig_save_dir+'t_startvsOH.png')
        save_plot(111, fig_save_dir+'exponentvsOH.png')



def create_all_plots_power05(folders,fig_save_dir, forced_exponent = None, forced_dt=None, t_end=None, h=0.05, rhof=0.9, plot_individual_plots=False, save_plots=True, linestyle="--"):
    if t_end is None:
        t_end = np.inf + np.zeros( len(folders))
    # preparte Oh_f values for plotting and saving
    unique_ohf = sorted({get_Ohf_from_folder_name(f) for f in folders})
    cmap = plt.get_cmap("tab10")
    ohf_to_color = {ohf: cmap(i % 10) for i, ohf in enumerate(unique_ohf)}
    Oh = []

    i = -1
    t_start = []
    D_list = []
    power_list =[]
    for f in folders:
        i +=1
        # load data and Oh
        t, z, r, v = load_data(f)
        l = get_Ohf_from_folder_name(f.split("/")[-1])
        if l<0.005:
            continue
        # setup color and labels for plotting
        color = ohf_to_color[l]
        label = r'$Oh = $' + f'{l}'+r" $h = $" + f'{h}'

        # apply filters to data
        mask = (r/np.sqrt(h)>1.5) & (t < t_end[i])
        if len(t[mask]) ==0:
            continue
        t_min = t[mask][0]
        t_o, r_o, v_o = t.copy(), r.copy(), v.copy()
        t, r, v = t[mask], r[mask], v[mask]
        sigma = 5
        if l > 1:
            sigma=10
        v_smooth = gaussian_filter1d(v, sigma=sigma)
        _, v_s = log_sampler(t, v, 50)
        t_s, r_s = log_sampler(t, r, 50)

        # fit data


        a, b, c, pcov = get_fit(t, r, cc=forced_exponent, bb=forced_dt)

        if c > 1.99: #or l>4.9: 
            print(f"for Ohf={l}: no fit found or skipped")
            continue
        print(f"Fit parameters for Ohf={l}: a={np.round(a, 2)}, dt={np.round(b, 2)}, c={np.round(c, 2)}")
        dt = b
        D = (a**2)/2
        D_list += [D]
        Oh.append(l)
        t_start.append(b)
        power_list.append(c)
        # if i<3:
        #     continue
        # plot r vs t
        create_plot(t_o,  r_o, 2, fmt=linestyle, color=color, label=label, alpha=0.7, 
                    xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', title=None)
        # plt.xlim(0, 5)
        
        # plot r vs t 
        create_plot(t_o, r_o, 3, fmt=linestyle, label=label, xlabel=r'$\tilde t$', ylabel=r'$\tilde{r}$', 
                    title=None, alpha=0.7, color=color, xscale="log", yscale="log")

        # plot r vs t log and corrected
        create_plot(t_o/(l**0.8), r_o, 4, fmt=linestyle, color=color, label=label, xlabel=r'$\tilde t - \tilde t_0$', ylabel=r'${\tilde{r}}/{\alpha}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2)
        
        create_plot(t-dt, r/a, 444, fmt=linestyle, color=color, label=label, xlabel=r'$\tilde t - \tilde t_0$', ylabel=r'${\tilde{r}}/{\alpha}$', 
                    title=None, alpha=0.7, xscale="log", yscale="log",  markersize=2)
        # plot TP velocity vs time
        create_plot(t-dt, 2*v/a , 9, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$2\tilde v(\tilde t)/{a}$', title=None, alpha=0.5, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t-dt, 2*v_smooth/a, 10, fmt='-', color=color, label=label, xlabel=r'$\tilde t-\tilde t_0$', 
                    ylabel=r'$2\tilde v(\tilde t)/{a}$', title=None, alpha=0.5, xscale="log", yscale="log",  markersize=0.7)
        create_plot(t_o, v_o, 11, fmt='-', color=color, label=label, xlabel=r'$\tilde t$', 
                    ylabel=r'$\tilde v(\tilde t)$)', title=None, alpha=0.5,markersize=0.7, xscale="log", yscale="log")
        plt.xlim(1e-3, 10)
        # plt.ylim(1e-2, 3)
        create_plot(t_o, z, 101, xlabel="t", ylabel="z",xscale="log", yscale="log", label=label, color=color, fmt=linestyle)
        create_plot(r_o, z, 102, xlabel="r", ylabel="z",xscale="log", yscale="log", label=label, color=color, fmt=linestyle)
        if plot_individual_plots:
            # plot single plots, corrected data r vst t and v vs t
            temp = np.linspace(min(t), max(t), 100)
            create_plot(t_o - dt, r_o/np.sqrt(h), 7, fmt=linestyle, color=color, label=label, xlabel=r'$\tilde t - \tilde t_0$', ylabel=r'${{r}}/\sqrt{hR}$', 
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
            

    # temp = np.linspace(1e-1, 80, 10000)
    # create_plot(temp, temp**0.5, 3, fmt="k--", alpha=0.5, label = r"$\sim t^{0.5}}$")
    # create_plot(temp, temp, 3, fmt="k--", alpha=0.75, label = r"$\sim t$")
    temp = np.linspace(1e-1, 3, 100)
    if save_plots:
        create_plot(temp, temp**0.4, 4, alpha = 0.8, fmt="k:", label = r"$r\sim t^{0.4}$")
        create_plot(temp, temp**0.5, 4, alpha = 0.8, fmt="k--", label = r"$r\sim t^{0.5}$")
        create_plot(temp, temp**0.5, 444, alpha = 0.8, fmt="k--", label = r"$r\sim t^{0.5}$")
        save_plot(444, fig_save_dir+'rvst_collapsed.png', dpi=300)
        save_plot(2, fig_save_dir+'rvst_originol.png', dpi=300)
        save_plot(3, fig_save_dir+'rvst_originol_log.png', dpi=300)
        save_plot(4, fig_save_dir+'rvst_corrected_log.png', dpi=300)
        temp = np.linspace(1e-2, max(t_o), 1000)
        create_plot(temp, temp, 101, alpha = 0.8, fmt="k:", label = r"$z\sim t^{1}$")
        temp = np.linspace(1e-1, max(r_o), 1000)
        create_plot(temp, temp**2, 102, alpha = 1, fmt="k:", label = r"$z\sim r^{2}$")
        create_plot(temp, temp, 102, alpha = 0.5, fmt="k--", label = r"$z\sim r$")
        save_plot(101, fig_save_dir+'zvst.png', dpi=300)
        save_plot(102, fig_save_dir+'zvsr.png', dpi=300)

        create_plot(temp, temp**0.5, 4, fmt="k--", alpha=1, label = r"$\sim t^{0.5}$")
        create_plot(temp, temp**-0.5, 9, fmt="k--", label = r"$\sim t^{-0.5}$")
        create_plot(temp, temp**-1, 10, alpha = 0.4, fmt="k:", label = r"$\sim t^{-1}$")
        create_plot(temp, temp**-(2/3), 10, alpha = 0.75, fmt="k-.", label = r"$\sim t^{-2/3}$")
        create_plot(temp, temp**-0.5, 10, fmt="k--", label = r"$\sim t^{-0.5}$")
        create_plot(temp, temp**-0.5, 11, fmt="k--", label = r"$\sim t^{-0.5}$")
    if save_plots:
        save_plot(9, fig_save_dir+'vvst_corrected.png', dpi=300)
        save_plot(10, fig_save_dir+'vvst_filtered.png', dpi=300)
        save_plot(11, fig_save_dir+'vvst_original.png', dpi=300)

    # plot D vs Oh
    alpha = 2.8**2
    beta = 0.15
    # R = 650e-6
    R = 1
    # h=1

    create_plot(np.array(Oh) * R/h, np.array(D_list)*0.9, 99, label ="h="+str(h), 
        fmt=".", xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", ylabel = r"$D/D_0\cdot \frac{\sqrt{\gamma_{1}+\gamma_2}}{\sqrt{\gamma_{drop}}}$")
    if save_plots:
        Oh_asymptotes = np.linspace(min(Oh), max(Oh)*10, 10000)
        print(Oh_asymptotes[0], Oh_asymptotes[-1])
        asymptote_low = 1/np.sqrt(alpha) * np.ones(len(Oh_asymptotes)) 
        asymptote_high = 1 / (beta * Oh_asymptotes * R/h)
        crit = (asymptote_high<asymptote_low)
        create_plot(Oh_asymptotes[crit]*R/h, asymptote_high[crit], 99, fmt = "k:", label=r"$\frac{D}{D_0} \sim\left(Oh(\frac{R}{h})\right)^{-1}$")
        create_plot(Oh_asymptotes[~crit]*R/h, asymptote_low[~crit], 99, fmt = "k--", label=r"$\frac{D}{D_0} \sim \frac{1}{\alpha}$")
        # create_plot(Oh_asymptotes * R / 0.05, get_theoretical_D(Oh_asymptotes, h=0.05), 99, fmt=":k", label="fit from paper, h=0.05", alpha=0.5)
        # create_plot(Oh_asymptotes * R / 0.1 , get_theoretical_D(Oh_asymptotes, h=0.1 ), 99, fmt="k.-", label="fit from paper, h=0.1", alpha=0.5)
        # create_plot(Oh_asymptotes * R / 0.03, get_theoretical_D(Oh_asymptotes, h=0.03), 99, fmt="--k", label="fit from paper, h=0.03", alpha=0.5)
        save_plot(99, fig_save_dir+'DvsOh.png', dpi=300)

    
    create_plot(Oh, power_list, 20, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$n$", label ="h="+str(h))
    if save_plots:
        save_plot(20, fig_save_dir+'nvsOh.png', dpi=300)
    
    
    create_plot(Oh, np.array(t_start)+1, 111, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", ylabel = r"$t_0$")
    


    if save_plots:
        save_plot(111, fig_save_dir+'t_startvsOH.png')

    
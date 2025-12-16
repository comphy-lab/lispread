import json
from libraries.plot_contact_line_lib import create_plot, save_plot, plot_triangle_with_labels
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


    # Two possible branches of the model, with alpha in front of psi
def model_plus(psi, D0, alpha):
    psi_eff = alpha * psi
    # D0 = 0.55
    return 0.5 * D0 * (-psi_eff + np.sqrt(psi_eff**2 + 4))

def model_minus(psi, D0, alpha):
    psi_eff = alpha * psi
    # D0 = 0.55
    return 0.5 * D0 * (-psi_eff - np.sqrt(psi_eff**2 + 4))
# plot_triangle_with_labels((0.1, 3/1.08), (0.1, 6.3/1.08), (0.1/(2.1**4), 6.3/1.08),  figure=98, l1=1, l2=3.5,
#     l1_center = ["right", "center"], l2_center = ["right", "bottom"])
# plot_triangle_with_labels((6e-3, 0.58), ( 6e-3, 0.93), ( 6e-3 * (0.93/0.58)**5, 0.93),  figure=97, l1=1, l2=5,
#     l1_center = ["right", "center"], l2_center = ["right", "bottom"])
plot_triangle_with_labels((3, 2e-1), ( 3, 5e-1), (3/5, 5e-1),  figure=99, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
plot_triangle_with_labels((3, 2e-1), ( 3, 5e-1), (3/5, 5e-1),  figure=199, l1=1, l2=2,
    l1_center = ["right", "center"], l2_center = ["right", "bottom"])
    


def do_all(data, Type="bubble", D0_list = None):
    Oh_f_data = data["Oh_f_list"]
    D_data = data["D_list"]
    t_start_data = data["t_start_list"]
    h_data = data["h_list"]
    Oh_d_data = data["Oh_d_list"]
    for j in range(len(Oh_f_data)):
        Oh_f_list = np.array(Oh_f_data[j])
        D_list =  np.array(D_data[j])
        t_start_list =  np.array(t_start_data[j])
        h =  h_data[j]
        print(h)
        Oh_d_list =  np.array(Oh_d_data[j])
        R = 1
        markers = {"0.01":"x", 
                    "0.005":"o",
                    "0.001":"s",
                    "0.0025":"D"}
        colors = {"0.006":"b", 
                    "0.015":"g",
                    "0.03":"r",
                    "0.05":"y",
                    "0.1":"m"}
        n = 1
        x = Oh_f_list[Oh_f_list > 0.005]**n*(1 + 0.05*np.sqrt(1/h)) # psi
        y = D_list[Oh_f_list > 0.005] # D


        # Fit both branches: parameters are [D0, alpha]
        popt_plus, _ = curve_fit(model_plus, x, y, p0=[1.0, 1.0])
        popt_minus, _ = curve_fit(model_minus, x, y, p0=[1.0, 1.0])

        D0_plus, alpha_plus = popt_plus
        D0_minus, alpha_minus = popt_minus

        # Compare residuals to decide which branch is better
        res_plus = np.sum((y - model_plus(x, D0_plus, alpha_plus))**2)
        res_minus = np.sum((y - model_minus(x, D0_minus, alpha_minus))**2)

        if True:
            D0_fit = D0_plus
            alpha_fit = alpha_plus
            model = model_plus
        else:
            D0_fit = D0_minus
            alpha_fit = alpha_minus
            model = model_minus

        print("Best D0 =", D0_fit)
        print("Best alpha =", alpha_fit)

        # Evaluate fitted curve
        x_fit = np.linspace(0.01, x.max(), 200)
        y_fit = model(x_fit, D0_fit, alpha_fit)
        
        plt.figure(98)
        plt.scatter(h, alpha_fit)
        plt.xlabel("h")
        plt.ylabel("Fitted alpha")
        plt.xscale("log")
        plt.yscale("log")
        plt.figure(97)
        plt.scatter(h, D0_fit)
        plt.xlabel("h")
        plt.ylabel("Fitted D0")
        plt.xscale("log")
        plt.yscale("log")
        # Create the fitted curve
        
        for i in range(len(Oh_d_list)):
            # print(Oh_d_list)
            _ = str(Oh_d_list[i])
            if _ == "0.00508":
                _ = "0.005"
            fmt = markers[_]+colors[str(h)]
            # print(fmt)
            if i <4:
                temp_label = "h="+str(h)+", Oh_d="+ _
            else:    
                temp_label = None
            #     continue
            if D0_list is not None:
                create_plot(Oh_f_list[i]**n *(1), D_list[i]/D_list[Oh_f_list==0.5][0]/2.5, 199, label =temp_label, alpha = 0.6,  # 0.9 therm to account for difference paper D0 and our D0 in surface tension
                            fmt=fmt, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", 
                            ylabel = r"$D/D_{0}$", markerfacecolor='none', markeredgewidth=1)
                create_plot(Oh_f_list[i]**n *(1+0.1*np.sqrt(1/h)), D_list[i]/D_list[Oh_f_list>5e-3][0], 99, label =temp_label, alpha = 0.6,  # 0.9 therm to account for difference paper D0 and our D0 in surface tension
                            fmt=fmt, xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot (1+0.05\sqrt{R/h})$", 
                            ylabel = r"$D/D_{0\, fit}$", markerfacecolor='none', markeredgewidth=1)
            else:
                create_plot(Oh_f_list[i]**n *(1), D_list[i], 199, label =temp_label, alpha = 0.6,  # 0.9 therm to account for difference paper D0 and our D0 in surface tension
                            fmt=fmt, xscale="log", yscale="log", xlabel=r"$Oh_{film}$", 
                            ylabel = r"$D/D_0$", markerfacecolor='none', markeredgewidth=1)
                create_plot(Oh_f_list[i]**n *(1+0.1*np.sqrt(1/h)), D_list[i], 99, label =temp_label, alpha = 0.6,  # 0.9 therm to account for difference paper D0 and our D0 in surface tension
                            fmt=fmt, xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot (1+0.05\sqrt{R/h})$", 
                            ylabel = r"$D/D_0$", markerfacecolor='none', markeredgewidth=1)
        # OHRh_Nath_self = np.array([145.72436405, 72.86218203, 14.4222051, 7.21110255, 2.85439476, 0.75115652])
        # D_Nath_self =  np.array([0.10075624, 0.1222998,  0.19366557, 0.27575631, 0.31608867, 0.36738312])

        # create_plot(OHRh_Nath_self* np.sqrt(0.7/0.6) , D_Nath_self* np.sqrt(0.72/0.6) , 199, label ="Nath & Queré \n processed myself", alpha = 0.75,  
        #             fmt="kv", xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", 
        #             ylabel = r"$D/D_0$", markeredgewidth=1, markerfacecolor='none')
        
    plt.figure(99)
    ax = plt.gca()
    leg = ax.get_legend()
    if leg:
        leg.remove()
    plt.figure(199)
    ax = plt.gca()
    leg = ax.get_legend()
    if leg:
        leg.remove()
    save_plot(99, "figures/water/find_scaling_of_D/"+'DvsOh1pRh.png', dpi=300)
    save_plot(199, "figures/water/find_scaling_of_D/"+'DvsOh.png', dpi=300)
    save_plot(97, "figures/water/find_scaling_of_D/"+'D0_fit_vs_h.png', dpi=300)
    save_plot(98, "figures/water/find_scaling_of_D/"+'alpha_vs_h.png', dpi=300)


    """
    """
    ##! Create custom legend 
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

    # handles.append(plt.Line2D([0], [0], color="black", marker=">", linestyle="none",
    # markerfacecolor='none', markeredgewidth=1))
    # labels.append(r"Experiments (Nath & Quéré)")

    # handles.append(plt.Line2D([0], [0], color="black", marker="v", linestyle="none",
    # markerfacecolor='none', markeredgewidth=1))
    # labels.append("Experiments (Nath & Quéré)\nPost-processed myself")

    # handles.append(plt.Line2D([0], [0], color="black", linestyle="--"))
    # labels.append(r"$\frac{D}{D_0} \sim 1$")

    # handles.append(plt.Line2D([0], [0], color="black", linestyle=":"))
    # labels.append(r"$\frac{D}{D_0} \sim\left(Oh(\frac{R}{h})\right)^{-1}$")
    # for i in range(len(h_list)):
    #     handles.append(plt.Line2D([0], [0], color=colors[i], marker="o", linestyle="none"))
    #     labels.append(f"$h = {h_list[i]}$")

    ax.legend([])  # This removes the original legend
    ax.legend(handles=handles, labels=labels, loc='best', fontsize=14, markerscale=1.5,)# Add the custom legend
    # plt.xlim(1e-1, 1.5e3)
    save_plot(1, "figures/water/find_scaling_of_D/"+'DvsOh_legend.png', dpi=300)
    # plt.close('all')
    print(t_start_data)

with open("saved_lists.json", "r") as f:
    data = json.load(f)
    
do_all(data, D0_list = 
    
    [1]*100)
# with open("bubble.json", "r") as f:
#     data = json.load(f)
# do_all(data)
import numpy as np
import matplotlib.pyplot as plt
def save_plot(n_fig, filename, dpi=300):
    plt.figure(n_fig)
    plt.grid(True, which='both', alpha=0.3)
    # plt.tight_layout()
    plt.savefig(filename, dpi=dpi)


def create_plot(x, y, n_fig=None, color=None, fmt="-", label=None, xlabel=None, ylabel=None, title=None, 
                xscale=None, yscale=None, alpha=1.0, markersize=10, subplot=None,
                markerfacecolor=None, markeredgewidth=None):
    if n_fig is not None:
        plt.figure(n_fig, figsize=(8, 6))
    if subplot is not None:
        plt.subplot(subplot)
    if color is not None:
        plt.plot(x, y, fmt, color=color, label=label, alpha=alpha, markersize=markersize, 
                markerfacecolor=markerfacecolor, markeredgewidth=markeredgewidth)
        plt.grid(True, which="both", alpha=0.3)
    else:
        plt.plot(x, y, fmt, label=label, alpha=alpha, markersize=markersize,
                markerfacecolor=markerfacecolor, markeredgewidth=markeredgewidth)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=20)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=20)
    if title is not None:   
        plt.title(title)
    if xscale is not None:
        plt.xscale(xscale)
    if yscale is not None:
        plt.yscale(yscale)
    if label is not None:
        plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    ax = plt.gca()
    ax.tick_params(axis="both", which="major", labelsize=14)



data = np.array([[0.003048851770038303, 10.411665709419992],
[0.003016032087673158, 11.356802275639202],
[0.002999754969228218, 12.542460712234641],
[0.003048851770038303, 15.927819821709175],
[0.002999754969228218, 18.833568438129195],
[0.002999754969228218, 20.22692756177921],
[0.0029835656961964495, 21.58896418859448],
[6.70018750350959, 489.8092180855831],
[6.628062637416333, 542.6269352141263],
[6.521328464812761, 590.0509145977018],
[6.4511289454667535, 737.7760082683297],
[6.5213284648127745, 886.0114882573647],
[6.5213284648127745, 945.6735449439157],
[5.634836460951345, 954.5185362365621]])



x = data[:,0] * 1e-3
y = data[:,1] * 1e-6
N = int(len(x)/2)
gamma = 72e-3
R = 0.65e-3
rho = 1e3
h = 20e-6
D0 = np.sqrt(gamma*R/rho)
eta = np.array([5, 19, 48, 96, 485, 970][::-1])*1e-3
D_list = []
for i in range(1, N):
    x1, x2 = x[i], x[i + N]
    y1, y2 = y[i], y[i + N]
    create_plot((x1, x2), (y1, y2), 98, xscale="log", yscale= "log", xlabel = "t(s)", ylabel = "r(m)")
    plt.xscale("log")
    plt.yscale("log")
    D1, D2 = ((y1**2 / x1)/2 , (y2**2 / x2)/2 )
    D = np.mean([D1, D2])#/np.sqrt(2)
    print(eta[i-1], D/D0)
    D_list += [D/D0]
D_list = np.array(D_list)

create_plot(eta/np.sqrt(rho*gamma*R)*R/h * np.sqrt(0.72/0.6) , D_list* np.sqrt(0.72/0.6)  , 99, label ="Nath & Queré processed myself", alpha = 0.75, xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", fmt = ".",
            ylabel = r"$D/D_0$", markeredgewidth=1, markerfacecolor='none')
plt.ylim(0.05, 0.5)
plt.xlim(0.1, 1000)


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
                    [202.37546008116516, 0.08529694459231732]])* np.sqrt(0.72/0.6)  



create_plot(data_Nath[:,0], data_Nath[:,1], 99, label ="Nath & Queré", alpha = 0.75,  
            fmt="ks", xscale="log", yscale="log", xlabel=r"$Oh_{film}\cdot R/h$", 
            ylabel = r"$D/D_0$", markeredgewidth=1, markerfacecolor='none')

print(eta/np.sqrt(rho*gamma*R)*R/h)
print(D_list)

save_plot(99, "DvsOhRh.png")
save_plot(98, "rvst_fit.png")
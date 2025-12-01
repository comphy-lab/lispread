import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
import glob
from scipy.interpolate import interp1d

def remove_isolated_points(mask, distance_threshold=2):
    # Create a copy of the mask array to store modifications
    mask_copy = mask.copy()
    n = len(mask)

    # Function to check if a point is isolated
    def is_isolated(i):
        # Check neighbors within the distance_threshold on both sides
        for offset in range(1, distance_threshold + 1):
            # Check the previous index
            if i - offset >= 0 and mask[i - offset] == 1:
                return False
            # Check the next index
            if i + offset < n and mask[i + offset] == 1:
                return False
        return True

    # Iterate over each point in the mask
    for i in range(n):
        # If the current point is true and isolated, set it to False
        if mask[i] == 1 and is_isolated(i):
            mask_copy[i] = 0

    return mask_copy
def kalman_1d_velocity(v, Q=1e-5, R=1e-2, x0=None, P0=1.0):
    """
    Simple 1D Kalman filter for a scalar signal (here: velocity).
    Q: process noise variance (higher -> more responsive)
    R: measurement noise variance (higher -> smoother)
    x0: initial estimate (defaults to first sample)
    P0: initial variance
    """
    v = np.asarray(v, dtype=float)
    x = v[0] if x0 is None else float(x0)  # state = filtered velocity
    P = float(P0)
    out = np.empty_like(v)

    for i, zk in enumerate(v):
        # predict
        P = P + Q
        # update
        K = P / (P + R)
        x = x + K * (zk - x)
        P = (1 - K) * P
        out[i] = x
    return out
def save_plot(n_fig, filename, dpi=300):
    plt.figure(n_fig)
    plt.grid(True, which='both', alpha=0.3)
    # plt.tight_layout()
    plt.savefig(filename, dpi=dpi)

def make_Oh_h_legend(Oh, h, colors, linestyles, n_fig=None, linewidth=2, Oh_string=" Oh = "):
    assert len(h) == len(linestyles)
    assert len(Oh) == len(colors)
    if n_fig is not None:
        plt.figure(n_fig)
    
    handles, labels = [], []
    ax = plt.gca()

    for i in range(len(h)):
        handles.append(plt.Line2D([0], [0], color="black", linestyle=linestyles[i], linewidth=linewidth))
        labels.append(r"$\tilde h = $"+str(h[i]))
    for i in range(len(Oh)):
        handles.append(plt.Line2D([0], [0], color=colors[i], linestyle="-", linewidth=linewidth))
        labels.append(f"${Oh_string}{Oh[i]}$")


    # Remove the default legend
    ax.legend([])  # This removes the original legend

    # Add the custom legend
    ax.legend(handles=handles, labels=labels, loc='best')

def plot_triangle_with_labels(corner1, corner2, corner3, figure=None, l1 = None, l2=None, l1_center = ["left", "bottom"],  l2_center = ["left", "bottom"]):
    """
    Plots a triangle with the given corner coordinates and labels the lengths of the sides.

    Parameters:
    corner1, corner2, corner3 : tuple
        Coordinates of the three corners of the triangle (x, y).
    """
    if figure is not None:
        plt.figure(figure)
    # Unpack the corner points
    x1, y1 = corner1
    x2, y2 = corner2
    x3, y3 = corner3

    # Calculate the lengths of the sides
    side1 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)  # Distance between corner1 and corner2
    side2 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2)  # Distance between corner2 and corner3
    side3 = np.sqrt((x1 - x3)**2 + (y1 - y3)**2)  # Distance between corner1 and corner3

    # Create a figure

    # Plot the triangle
    plt.plot([x1, x2], [y1, y2], color='black', alpha=1)  # Line between corner1 and corner2
    plt.plot([x2, x3], [y2, y3], color='black', alpha=1)  # Line between corner2 and corner3
    plt.plot([x3, x1], [y3, y1], color='black', alpha=1)  # Line between corner3 and corner1

    # Annotate the lengths of the sides
    mid_x1 = (x1 + x2) / 2
    mid_y1 = (y1 + y2) / 2
    mid_x2 = (x2 + x3) / 2
    mid_y2 = (y2 + y3) / 2
    mid_x3 = (x1 + x3) / 2
    mid_y3 = (y1 + y3) / 2

    # Label the lengths of the sides
    plt.text(mid_x1, mid_y1, l1, fontsize=12, ha=l1_center[0], va=l1_center[1])
    plt.text(mid_x2, mid_y2, l2, fontsize=12, ha=l2_center[0], va=l2_center[1])


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

def load_folders(folder_names):
    folders = []
    for folder_name in folder_names:
        folder_name = os.path.join("data", folder_name)
        # collect only subdirectories
        subfolders = [
            os.path.join(folder_name, f)
            for f in os.listdir(folder_name)
            if os.path.isdir(os.path.join(folder_name, f))
        ]
        folders += subfolders

    # --- extract numeric value after "Ohf_" ---
    def get_ohf_value(path):
        base = os.path.basename(path)
        match = re.search(r'Ohf_([\d\.p\-eE]+)', base)
        if match:
            # convert 0p08 → 0.08 etc.
            val = match.group(1).replace('p', '.')
            try:
                return float(val)
            except ValueError:
                return float('inf')
        return float('inf')

    folders = sorted(folders, key=get_ohf_value)
    return folders


# def ELS_func(t, tau, t0):
#     t = t - t0
#     tau = 100*tau
#     assert np.all(t > 0), "t - t0 must be positive in ELS_func"
#     return t/tau * np.log(tau/t)
def ELS_func(t, tau, t0):
    return (t-t0)/tau

def fit_ELS_law(t, r, dt = None):    
    if dt is not None:
        bounds = ([1e-6, dt-1e-6], [np.inf, dt])
    else:
        bounds = ([1e-12, 0], [np.inf, np.min(t)-1e-6])
    r_fit = r/ np.log(1/r)
    popt, pcov = curve_fit(ELS_func, t,  r/ np.log(1/r), bounds=bounds, maxfev=20000)
    tau, t0 = popt
    print(tau, t0)
    # for i in range(1000):
    #     tau, t0 = popt
    #     rtemp = np.linspace(np.log(r[0]) , np.log(r[-1]), N)
    #     xfit = t0 + np.exp(xtemp)
    #     yfit = interp1d(x, y, kind='cubic',  fill_value='extrapolate')(xfit) 
    #     r_predicted = func(xfit, a, t0, n)
    #     popt, pcov = curve_fit(func, xfit, yfit, bounds=bounds, maxfev=1000, sigma = 1/r_predicted**4, p0=popt)
    return tau, t0, pcov

# # --- loader ---
def load_data(folder):
    if os.path.exists(folder + '/tp_data.csv'):
        filename = "tp_data.csv"
    elif os.path.exists(folder + '/tp_data.npz'):
        filename = "tp_data.npz"
    else:
        assert False, "data file not found"
    print("loaded data file:", filename)
    data = np.loadtxt(folder + '/' + filename)
    t =  data[:,0]
    zTP = data[:,1]
    rTP = data[:,2]
    vTP = data[:,3]     
    try:
        theta1 = data[:,4]
        theta2 = data[:,5]   
        return np.array(t), np.array(zTP), np.array(rTP), np.array(vTP), np.array(theta1), np.array(theta2)
    except:
        return np.array(t), np.array(zTP), np.array(rTP), np.array(vTP)

def get_Ohf_from_folder_name(folder_name):
    match = re.search(r"Ohf_([0-9p\-e]+)", folder_name)
    assert match, "Ohf not found in folder name"
    return float(match.group(1).replace("p", "."))

def lin_func(x, a, b):
    return a * x + b

def get_lin_fit(x, y, bb=None):
    # Define linear function

    # Fit the function to the data
    if bb is None:
        popt, _ = curve_fit(lin_func, x, y)
    else:
        lower_bounds = [-np.inf, bb-1e-6]
        upper_bounds = [np.inf, bb+1e-6]
        bounds = (lower_bounds, upper_bounds)
        popt, _ = curve_fit(lin_func, x, y, bounds=bounds)

    # Extract slope (a) and intercept (b)
    a, b = popt
    return a, b


def func(t, a, t0, n):
    return a * (t - t0)**n

def func_no_t0(t, a, t0, n):
    return a * (t)**n

def get_fit(x, y, bb=None, cc=None, init_cond=None, aa=None, N=1000):
    if bb is None and cc is None:
        lower_bounds = [-np.inf, 0 , -2]  # no lower restriction
        upper_bounds = [np.inf, np.min(x), 2]     # no upper restriction

    elif bb is not None and cc is None:
        lower_bounds = [-np.inf, bb - 1e-6, -2] # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, ]     # no upper restriction

    elif bb is None and cc is not None:
        lower_bounds = [-np.inf, 0 , cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, np.min(x), cc + 1e-6]     # no upper restriction

    else:
        lower_bounds = [-np.inf, bb - 1e-6, cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, cc + 1e-6]     # no upper restriction
    
    if aa is not None:
        lower_bounds[0] = aa - 1e-6
        upper_bounds[0] = aa + 1e-6
        


    if bb is None:
        bounds = (lower_bounds, upper_bounds)
        # Fit the function to the data
        popt, pcov = curve_fit(func, x, y, bounds=bounds, maxfev=20000)
        
        for i in range(N):
            a, t0, n = popt 
            xtemp = np.linspace(np.log(x[0]-t0) , np.log(x[-1] - t0), N)
            xfit = t0 + np.exp(xtemp)
            yfit = interp1d(x, y, kind='cubic',  fill_value='extrapolate')(xfit) 
            r_predicted = func(xfit, a, t0, n)
            popt, pcov = curve_fit(func, xfit, yfit, bounds=bounds, maxfev=1000, sigma = 1/r_predicted, p0=popt)
    else:
        bounds = (lower_bounds, upper_bounds)
        print("dt was forced")
        # Fit the function to the data
        popt, pcov = curve_fit(func_no_t0, x-bb, y, bounds=bounds, maxfev=20000)
        a, _, n = popt 
        r_predicted = func_no_t0(x-bb, a, bb, n)
        popt, pcov = curve_fit(func_no_t0, x-bb, y, bounds=bounds, maxfev=20000, sigma = 1/r_predicted, p0=popt)
        a, _, c  = popt
        return a, bb, c, pcov

    # Extract slope (a) and intercept (b)
    a, bb, c  = popt

    return a, bb, c, pcov

def get_fit_old(x, y, bb=None, cc=None, init_cond=None, ):
    if bb is None and cc is None:
        lower_bounds = [-np.inf, 0 , -2]  # no lower restriction
        upper_bounds = [np.inf, np.min(x), 2]     # no upper restriction

    elif bb is not None and cc is None:
        lower_bounds = [-np.inf, bb - 1e-6, -2] # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, ]     # no upper restriction

    elif bb is None and cc is not None:
        lower_bounds = [-np.inf, 0 , cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, np.min(x), cc + 1e-6]     # no upper restriction

    else:
        lower_bounds = [-np.inf, bb - 1e-6, cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, cc + 1e-6]     # no upper restriction
    
    bounds = (lower_bounds, upper_bounds)
    # Fit the function to the data
    popt, pcov = curve_fit(func, x, y, bounds=bounds, maxfev=20000, sigma=1/y+1e-6)

    # Extract slope (a) and intercept (b)
    a, bb,c  = popt

    return a, bb, c, pcov
def func_log(x, log_alpha, t0, n):
    # Function form: log(r) = log(alpha) + n * log(abs(t - t0))
    if np.any(x - t0 <= 0):
        assert False, "in trying fit x - t0 <= 0"
    return log_alpha + n * np.log(x - t0)

def get_fit_log(x, y, bb=None, cc=None, init_cond=None, dx_fit=None):
    """
    Does not work!!!!!!!
    """
    # Logarithmic transformation of y and x
    dx = x[1] - [0]
    log_x = np.log(x) 
    log_y = np.log(y)  
    if dx_fit is None:
        dx_fit = np.max(log_x[1:] - log_x[:-1])
    print(dx_fit)
    # ref_x = np.arange(np.min(log_x), np.max(log_x), dx_fit)
    ref_x = np.linspace(np.min(log_x), np.max(log_x), 50)
    ref_y = interp1d(log_x, log_y, kind='linear')(ref_x)
    
    # print("Fitting data points:", (ref_x))
    if bb is None and cc is None:
        lower_bounds = [-np.inf, np.min(ref_x) - 1e-6, -2]  # no lower restriction
        upper_bounds = [np.inf, np.min(ref_x), 2]     # no upper restriction

    elif bb is not None and cc is None:
        lower_bounds = [-np.inf, bb - 1e-6, -2] # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, ]     # no upper restriction

    elif bb is None and cc is not None:
        lower_bounds = [-np.inf, np.min(ref_x) - 1e-6, cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, np.min(ref_x), cc + 1e-6]     # no upper restriction

    else:
        lower_bounds = [-np.inf, bb - 1e-6, cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, cc + 1e-6]     # no upper restriction

    bounds = (lower_bounds, upper_bounds)

    # Fit the function to the transformed (log-transformed) data
    popt, pcov = curve_fit(func_log, ref_x, ref_y, bounds=bounds, maxfev=20000)

    # Extract fitted parameters: log_alpha, t0, n
    log_alpha, t0, n = popt
    
    # Exponentiate log_alpha to get alpha
    alpha = np.exp(log_alpha)

    return alpha, t0, n, pcov



def log_sampler(t, r, npoints=200, tmin=None, tmax=None):
    """
    Resample (t, r) data onto a log-spaced time grid.
    
    Parameters
    ----------
    t : array
        Original time values (linear sampling).
    r : array
        Original data values.
    npoints : int
        Number of log-spaced points to sample.
    tmin, tmax : float or None
        Range for log sampling. Defaults to min(t[t>0]) and max(t).
    
    Returns
    -------
    t_new, r_new : arrays
        Resampled arrays with log-spaced time.
    """
    mask = (t > 0) & (r > 0)  # avoid log(0)
    t, r = np.asarray(t[mask]), np.asarray(r[mask])

    if tmin is None: 
        tmin = t.min()
    if tmax is None:
        tmax = t.max()

    # log-spaced times
    t_new = np.logspace(np.log10(tmin), np.log10(tmax), npoints)

    # interpolate r onto new grid (log interpolation is safer for power laws)
    r_new = np.exp(np.interp(np.log(t_new), np.log(t), np.log(r)))
    
    return t_new, r_new


def get_D0(R, rho, gamma):
    return np.sqrt(gamma * R / rho)

def get_psi(eta_o, R, h, rho, gamma):
    return eta_o * np.sqrt(R) / (h * np.sqrt(rho * gamma))

def predict_D(eta_o, R, h, rho, gamma, alpha, beta):
    D0 = get_D0(R, rho, gamma)
    psi = get_psi(eta_o, R, h, rho, gamma)

    # Positive root of alpha x^2 + beta psi x - 1 = 0
    A = alpha**2
    B = beta * psi * D0
    C = -D0**2
    disc = B**2 - 4 * A * C
    x = abs(-B + np.sqrt(disc)) / (2.0 * A)
    return x 

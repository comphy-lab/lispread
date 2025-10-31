import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import re
from scipy.ndimage import gaussian_filter1d
import glob
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
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi)

def make_Oh_h_legend(Oh, h, colors, linestyles, n_fig=None, linewidth=2):
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
        labels.append(f"$ Oh = {Oh[i]}$")


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


def create_plot(x, y, n_fig=None, color=None, fmt="-", label=None, xlabel=None, ylabel=None, title=None, xscale=None, yscale=None, alpha=1.0, markersize=10, subplot=None):
    if n_fig is not None:
        plt.figure(n_fig, figsize=(8, 6))
    if subplot is not None:
        plt.subplot(subplot)
    if color is not None:
        plt.plot(x, y, fmt, color=color, label=label, alpha=alpha, markersize=markersize)
        plt.grid(True, which="both", alpha=0.3)
    else:
        plt.plot(x, y, fmt, label=label, alpha=alpha, markersize=markersize)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=14)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=16)
    if title is not None:   
        plt.title(title)
    if xscale is not None:
        plt.xscale(xscale)
    if yscale is not None:
        plt.yscale(yscale)
    if label is not None:
        plt.legend()
    plt.grid(True)

def load_folders(folder_names):
    folders = []
    for folder_name in folder_names:
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



# # --- loader ---
def load_data(folder):
    print("loading data")
    matches = glob.glob(os.path.join(folder, "[0-9][0-9][0-9][0-9]_X0Y0V0.dat"))
    print(matches)
    if os.path.exists(folder + '/tp_data.npz') and not matches:
        filename = "tp_data.npz"
    elif not matches:
        assert False, "no datafile found"
    elif not os.path.exists(folder + '/tp_data.npz') and len(matches)==1:
        filename = matches[0].split("/")[-1]
    else:
        assert False, "multiple datafiles found"
    print(filename)
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


def func(x, a, b, c):
    return a * (np.abs(x - b))**c

def get_fit(x, y, bb=None, cc=None, init_cond=None):
    if bb is None and cc is None:
        lower_bounds = [-np.inf, -np.inf , -2]  # no lower restriction
        upper_bounds = [np.inf, np.min(x), 2]     # no upper restriction

    elif bb is not None and cc is None:
        lower_bounds = [-np.inf, bb - 1e-6, -2] # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, ]     # no upper restriction

    elif bb is None and cc is not None:
        lower_bounds = [-np.inf, -np.inf , cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, np.min(x), cc + 1e-6]     # no upper restriction

    else:
        lower_bounds = [-np.inf, bb - 1e-6, cc - 1e-6]  # no lower restriction
        upper_bounds = [np.inf, bb + 1e-6, cc + 1e-6]     # no upper restriction


    
    bounds = (lower_bounds, upper_bounds)
    # Fit the function to the data
    popt, pcov = curve_fit(func, x, y, bounds=bounds, maxfev=20000)

    # Extract slope (a) and intercept (b)
    a, bb,c  = popt

    return a, bb, c, pcov


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

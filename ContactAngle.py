import numpy as np
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
import math
import pandas as pd

# --- Plot style setup ---
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.usetex'] = True

# ===============================================================
# Function: Extract interface points from simulation snapshot
# ===============================================================
def gettingFacets(filename):
    exe = ["./getFacet1", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp = stderr.decode("utf-8").split("\n")

    interface = []
    skip = False
    if len(temp) > 1e2:  # ensure valid output
        for n in range(len(temp) - 1):
            parts = temp[n].split(" ")
            if parts == ['']:
                skip = False
                continue
            if not skip:
                next_parts = temp[n + 1].split(" ")
                r1, z1 = float(parts[1]), float(parts[0])
                r2, z2 = float(next_parts[1]), float(next_parts[0])
                midpoint = np.array([-(r1 + r2) / 2, (z1 + z2) / 2])
                interface.append(midpoint)

                r0 = next((r for r, z in interface if z < 1e-1), None)
                if r0 is not None:
                    interface.sort(
                        key=lambda point: math.sqrt((point[0] - r0)**2 + point[1]**2)
                    )
                skip = True
    return interface

# ===============================================================
# Function: Compute arc length s and local interface angle θ(s)
# ===============================================================
def calculate_distances(interface):
    if not interface:
        return [], []
    interface_np = np.array(interface)
    diffs = np.diff(interface_np, axis=0)
    distances = np.sqrt(np.sum(diffs**2, axis=1))
    s = np.concatenate([[0], np.cumsum(distances)])
    r = interface_np[:, 0]
    z = interface_np[:, 1]
    dr_ds = np.gradient(r, s)
    dz_ds = np.gradient(z, s)
    theta = np.arctan2(dz_ds, dr_ds)
    return s, theta

# ===============================================================
# Plot several interface shapes and angle profiles
# ===============================================================
snapshots = np.arange(0, 1, 0.05)
interfaces, s_list, theta_list, t_list = [], [], [], []

for t in snapshots:
    print(t)
    place = f"/home/mark/lispread/Results/2025_10_17_Ohd_5p08e-3_Ohf_0p2_Ohe_9p1e-5_rho_d_1_rho_f_0p9_rho_e_1p2e-3_s1_0p33_s2_0p67_hf_0p05_Ldomain_5_delta_0p01_MaxLevel_11/intermediate/snapshot-{t:05.4f}"
    interface = gettingFacets(place)
    interfaces.append(interface)

    s, theta = calculate_distances(interface)
    theta_deg = np.degrees(theta)
    t_list.append(t)
    s_list.append(s)
    print(theta_deg)
    theta_list.append(theta_deg)

# --- Plot geometry and angles ---
fig, axs = plt.subplots(2, 2, figsize=(10, 6))
for t, theta in zip(t_list, theta_list):
    axs[0, 0].plot(t, theta, '.-')
# for s, theta in zip(s_list, theta_list):
#     axs[0, 0].plot(s, theta, '-')
# # θ(s)
# for s, theta in zip(s_list, theta_list):
#     axs[0, 0].plot(s, theta, '-')
# axs[0, 0].axvline(x=np.arcsin(0.3), color='r', linestyle='--')
# axs[0, 0].set_xlabel('s', fontsize=20)
# axs[0, 0].set_ylabel(r'$\theta$', fontsize=20)
# axs[0, 0].legend([f't={t}' for t in snapshots])
# axs[0, 0].grid(True)

# # s(z)
# for interface, s in zip(interfaces, s_list):
#     z = [p[1] for p in interface]
#     axs[0, 1].plot(z, s, '-')
# axs[0, 1].axvline(x=0.3, color='r', linestyle='--')
# axs[0, 1].set_xlabel('h', fontsize=20)
# axs[0, 1].set_ylabel('s', fontsize=20)
# axs[0, 1].legend([f't={t}' for t in snapshots])
# axs[0, 1].grid(True)

# # θ(z)
# for interface, theta in zip(interfaces, theta_list):
#     z = [p[1] for p in interface]
#     axs[1, 0].plot(z, theta, '-')
# axs[1, 0].axvline(x=0.3, color='r', linestyle='--')
# axs[1, 0].set_xlabel('h', fontsize=20)
# axs[1, 0].set_ylabel(r'$\theta$', fontsize=20)
# axs[1, 0].legend([f't={t}' for t in snapshots])
# axs[1, 0].grid(True)

# # r(z) shape
# for interface in interfaces:
#     r = [p[0] for p in interface]
#     z = [p[1] for p in interface]
#     axs[1, 1].plot(r, z, '-')
# axs[1, 1].axhline(y=0.3, color='r', linestyle='--')
# axs[1, 1].set_xlabel('r', fontsize=20)
# axs[1, 1].set_ylabel('h', fontsize=20)
# axs[1, 1].grid(True)

# plt.savefig('no_young_test.png')
# plt.show()

# # ===============================================================
# # Compute contact angle vs time (simulation only)
# # ===============================================================
# delZ = 2e-2
# nGFS = 1000
# contact_angle, t_values = [], []

# for ti in range(nGFS):
#     t = ti * 1e-1
#     place = f"test_young_50/snapshot-{t:05.4f}"
#     interface = gettingFacets(place)
#     if not interface:
#         continue

#     z = [p[1] for p in interface]
#     s, theta = calculate_distances(interface)
#     theta_deg = np.degrees(theta)

#     for i in range(len(theta_deg)):
#         if abs(z[i] - 0.3) < delZ:
#             contact_angle.append(theta_deg[i])
#             t_values.append(t)
#             break

# # --- Rescale time (optional) ---
# t0 = 3.38
# t_values = [i * t0 for i in t_values]

# # --- Plot θ(t) ---
# plt.figure()
# plt.plot(t_values, contact_angle, marker='o', linestyle='-')
# plt.grid(True)
# plt.xlabel('t (ms)', fontsize=18)
# plt.ylabel(r'$\theta$ (deg)', fontsize=18)
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.legend(['Simulation'])
# plt.subplots_adjust(bottom=0.15)
plt.savefig('contact_angle_young_70.png')
plt.show()

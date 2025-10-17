import numpy as np

def get_Oh(mu, rho, eta, L):
    Oh = mu/np.sqrt(rho*L*eta) # Ohnesorge number
    return Oh

def get_tau(rho, R, sigma):
    tau = np.sqrt(rho*R**3/sigma) # inertio-capillary time scale
    return tau
print("tau scale water: ", get_tau(1000, 0.65e-3, 72e-3))
mu_w = 1e-3 # dynamic viscosity of water
eta_w = 72e-3 # surface tension of water-air interface
rho_w = 1000 # density of water
L = 0.65e-3 # characteristic length scale

Ohw = get_Oh(mu_w, rho_w, eta_w, L)
print("Ohnesorge number water: ", Ohw)
rho_o = 900 # density of oil
for mu_o in np.array([5, 19, 48, 96, 485, 970])*1e-3:
    Oho = get_Oh(mu_o, rho_w, eta_w, L)
    print("Ohnesorge oil for sim: ", Oho)
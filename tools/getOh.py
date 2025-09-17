import numpy as np

def get_Oh(mu, rho, eta, L):
    Oh = mu/np.sqrt(rho*L*eta) # Ohnesorge number
    return Oh
mu_w = 1e-3 # dynamic viscosity of water
eta_w = 72e-3 # surface tension of water-air interface
eta_w = 1
rho_w = 1000 # density of water
L = 1.3e-3 # characteristic length scale
L = 1 # characteristic length scale
Ohw = get_Oh(mu_w, rho_w, eta_w, L)
print("Ohnesorge number water: ", Ohw)
mu_o = 1.2e-3 # dynamic viscosity of oil
eta_o = 15e-3 # surface tension of oil-air interface
eta_0 = 0.3 # surface tension of oil-water interface
rho_o = 900 # density of oil
Oho = get_Oh(mu_o, rho_o, eta_o, L)
print("Ohnesorge number oil: ", Oho)
mu_a = 1.8e-5 # dynamic viscosity of air
rho_a = 1.2 # density of air
Oha = get_Oh(mu_a, rho_a, eta_w, L)
print("Ohnesorge number air: ", Oha)
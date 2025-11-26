import numpy as np

def get_Oh(mu, R, gamma= 0.06, rho = 1000):
    return mu/(np.sqrt(rho * gamma * R))

V = np.array([0.1, 200])*1e-9
R = (3*V / (4*np.pi))**(1/3)
mu = np.array([5 , 970]) * 1e-3
mu_d = 1e-3
mu_e = 1.8e-5
h = 20e-6

min_Oh_f = get_Oh(min(mu), max(R))
max_Oh_f = get_Oh(max(mu), min(R))

min_Oh_d = get_Oh(mu_d, max(R))
max_Oh_d = get_Oh(mu_d, min(R))

min_Oh_e = get_Oh(mu_e, max(R))
max_Oh_e = get_Oh(mu_e, min(R))

min_h = h / max(R)
max_h = h / min(R)
print("R range: (",min(R)*1e3,"-", max(R)*1e3,")mm, factor = ", np.round(max(R)/min(R),2))
print("h range: (",min_h,"-", max_h,"), factor = ",             np.round(max_h/min_h,2))
print("Oh_f range: (",min_Oh_f,"-", max_Oh_f,"), factor = ",    np.round(max_Oh_f/min_Oh_f,2))
print("Oh_e range: (",min_Oh_e,"-", max_Oh_e,"), factor = ",    np.round(max_Oh_e/min_Oh_e,2))
print("Oh_d range: (",min_Oh_d,"-", max_Oh_d,"), factor = ",    np.round(max_Oh_d/min_Oh_d,2))

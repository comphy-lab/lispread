import numpy as np

Ldomain = 3
eta =1e-3 * 5 #(5 times water viscosity)      
rho = 1000
gamma=60e-3
R = 650e-6
# desired_cell_length = 1.67e-8
desired_cell_length = eta**2/(rho * gamma)/5
for MaxLevel in range(50):
    cells = 2**MaxLevel
    w_window = Ldomain * R
    hlow = w_window/ cells
    if hlow < desired_cell_length:
        break
else:
    print("No suitable MaxLevel found. (MaxLevel_crit>20)")
    print(hlow)
    exit()
print(f"Minimum MaxLevel to achieve cell length {desired_cell_length} is {MaxLevel} with cell length {hlow}")
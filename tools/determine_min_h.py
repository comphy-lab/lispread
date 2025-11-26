import numpy as np

Ldomain = 5
MaxLevel = 11
cells = 2**MaxLevel
hlow = 10/(cells/Ldomain)
print(hlow)
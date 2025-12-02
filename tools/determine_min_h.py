import numpy as np

Ldomain = 5
MaxLevel = 13
cells = 2**MaxLevel
hlow = 10/(cells/Ldomain)
print(hlow)
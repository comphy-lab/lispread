# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
# Last updated: 19-Nov-2020

import numpy as np
import matplotlib.pyplot as plt
folder = "verifyPaperTest_folder" # specify the folder where the data is stored

data = np.loadtxt(folder + '/tp_data.npz')
t =  data[:,0]
zTP = data[:,1]
rTP = data[:,2]
vTP = data[:,3]

plt.plot(t, rTP)
plt.xlabel('Time')
plt.ylabel('r')
plt.title('Contact Line Position vs Time')
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.savefig(folder + '/contact_line_position.png', dpi=300)
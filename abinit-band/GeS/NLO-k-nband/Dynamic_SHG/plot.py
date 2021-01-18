#%%
import matplotlib.pyplot as plt
import numpy as np

info = np.loadtxt('optic_2_0001_0001-linopt.out')

kpath = []
chi = []
for line in info:
    if '#' not in line:
        kpath.append(line[0])
        chi.append(line[1])
        
plt.xlim(0,6)
plt.xlabel('$\omega$ (eV)')
plt.plot(kpath, chi)
# %%
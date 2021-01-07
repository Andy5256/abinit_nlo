#%%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

with open('wannier90_band72.dat','r') as f:
    info = f.readlines()

kpoints = []
band = []
for i in info[:-1]:
    if i == '  \n':
        plt.plot(kpoints,band, c='r', linestyle = '-')
        kpoints = []
        band = []
        continue
    kpoints.append(float(i.split()[0]))
    band.append(float(i.split()[1])-3.4955)

# with open('BAND.dat','r') as f:
#     info = f.readlines()
# kpoints2  = []
# band2 = []
# for i in info:
#     if i.splitlines()[0] == "#":
#         continue
#     if i == ' \n':
#         plt.plot(kpoints2,band2, c='b')
#         kpoints2 = []
#         band2 = []

with open('wannier90_band.labelinfo72.dat', 'r') as f:
    info = f.readlines()

kpath = []
nkpt = []
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'
for i in info:
    nkpt.append(int(i.split()[1]))
    kpath.append(i.split()[0])
for i in nkpt:
    plt.vlines(kpoints[i-1], -20, 30)
kpath = list(''.join(kpath).replace('G', chr(915)))
kpath[-2] = 'Z|X'
kpath[-3] = 'Z|X'
plt.xticks(np.array(kpoints)[np.array(nkpt)-1], kpath)

plt.hlines(0, 0, kpoints[-1], linestyles='--')
plt.xlim(0,kpoints[-1])
plt.ylim(-18,25)

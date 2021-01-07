#%%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

with open('BAND.dat','r') as f:
    info = f.readlines()

# print(info)
kpoints2  = []
band2 = []

for idx, i in enumerate(info[:-1]):
    if i[0] == "#":
        continue
    if i == ' \n' and info[idx+1] == ' \n':
        plt.plot(kpoints2,band2, c='b')
        kpoints2 = []
        band2 = []
    kpoints2.append(i.split()[0])
    band2.append(i.split()[1])
    # print(len(kpoints2))
    # print(len(band2))

# %%

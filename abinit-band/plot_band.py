#%%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

with open('bando_DS2_EIG_AgGaS2', 'r') as f:
    info = f.readlines()

nkpts = int(info[0].split()[-3])
nbands = int(info[1].split()[3].replace(',', ''))

E_k = []
for i in range(nkpts):
    tmp = []
    for j in range(2, (nbands-1)//8+3):
        tmp += list(map(float, info[j + (2 + (nbands - 1) // 8) * i].split()))

    E_k.append(tmp)

E_k = np.array(E_k).T - 0.41633 * 27.2113845 *0

for Ei in E_k:
    # plt.plot(Ei + 0.14101 * 27.211 * 0.7, c='r') # graphene
    plt.plot(Ei - 0.14287 * 27.211, c='b') # AgGaS2
plt.ylim(-6,6)
plt.xlim(0,nkpts-1)
plt.hlines(0,xmin = 0, xmax = nkpts - 1, colors = 'k', linestyles='--')

xtick_list = []
highsymk = int
with open('bando_DS2_EBANDS_AgGaS2.agr') as f:
    info = f.readlines()
for idx, line in enumerate(info):
    if 'tick spec' in line:
        if not 'type' in line:
            highsymk = int(line.split()[3])
            for i in range(highsymk):
                xtick_list.append(int(info[idx+1+i].split()[5]))
xtick_list.append(nkpts)
# kpath = [chr(915), 'K', 'M', chr(915)] # kpath for graphene
kpath = [chr(915), 'X', 'Y', chr(931), chr(915), 'Z', chr(931) + '_1', 'N', 'P', 'Y_1', 'Z', 'X', 'P'] # kpath for AgGaS2
for i in xtick_list:
    plt.vlines(i, -10, 10, colors='k', )
    plt.vlines(i, -10, 10, )
plt.xticks(xtick_list, kpath)
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'
# plt.show()
# plt.savefig('graphene_goodkpath.png')
plt.savefig('Band_AgGaS2.png')


# %%

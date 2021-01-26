#%%
import matplotlib.pyplot as plt
import numpy as np

# a=str(12100)
b="4980_qmx_e0.1"
shift = 1.05
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
file_path = "E:\\Works\\xyz\\abinit-band\\GeS\\NLO-k-nband\\Permittivity\\Im_chi_11.dat"
info1 = np.loadtxt(file_path)
ax1.plot(info1[:,0], info1[:,1], label='openmx200k140bs_0.02')
abinit = np.loadtxt('optic_2_0001_0001-linopt'+b+'.out')
ax1.plot(abinit[:118,0], abinit[:118,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im $\epsilon$${_r}$$^{xx}$')
ax1.legend_ = None
ax1.legend()
plt.xlim(0,6)
plt.title('1L-GeS Im_chi_11')
ax2 = plt.subplot(122)
info2 = np.loadtxt('Re_chi_11.dat')
ax2.plot(info2[:,0], shift + info2[:,1], label='openmx200k140bs_0.02+'+str(shift))
abinit = np.loadtxt('optic_2_0001_0001-linopt'+b+'.out')
ax2.plot(abinit[119:238,0], abinit[119:238,1], label='abinit'+b)
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Re $\epsilon$${_r}$$^{xx}$')
ax2.legend()
plt.xlim(0,6)
plt.title('1L-GeS Re_chi_11')
ax2.legend()
plt.tight_layout()
plt.savefig('Chi_11_'+b+'_'+str(shift)+'.png')
# ax1.get_legend().remove()
# plt.show()
# %%

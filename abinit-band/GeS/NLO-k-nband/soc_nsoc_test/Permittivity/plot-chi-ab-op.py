#%%
import matplotlib.pyplot as plt
import numpy as np

# a=str(12100)
b="openmx"
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
# file_path = "E:\\Works\\xyz\\abinit-band\\GeS\\NLO-k-nband\\soc_nsoc_test\\Permittivity\\Im_chi_11_soc.dat"
openmx_soc = np.loadtxt('Im_chi_11_soc.dat')
ax1.plot(openmx_soc[:,0], openmx_soc[:,1], label='openmx_soc')
openmx_nsoc = np.loadtxt('Im_chi_11_nsoc.dat')
ax1.plot(openmx_nsoc[:,0], 2*openmx_nsoc[:,1], label='2*openmx_nsoc')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im $\epsilon$${_r}$$^{xx}$')
# ax1.legend_ = None
ax1.legend()
plt.xlim(0,6)
plt.title('1L-GeS Im_chi_11')
ax2 = plt.subplot(122)
openmx_soc = np.loadtxt('Re_chi_11_soc.dat')
ax2.plot(openmx_soc[:,0], openmx_soc[:,1], label='openmx_soc')
openmx_nsoc = np.loadtxt('Re_chi_11_nsoc.dat')
ax2.plot(openmx_nsoc[:,0], 2*openmx_nsoc[:,1], label='2*openmx_nsoc')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Re $\epsilon$${_r}$$^{xx}$')
ax2.legend()
plt.xlim(0,6)
plt.title('1L-GeS Re_chi_11')
ax2.legend()
plt.tight_layout()
plt.savefig('Chi_11_'+b+'.png')
# ax1.get_legend().remove()
# plt.show()
# %%

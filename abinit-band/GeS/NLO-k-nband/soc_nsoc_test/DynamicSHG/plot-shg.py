#%%
import matplotlib.pyplot as plt
import numpy as np

# a='_4980_e0.02'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
# openmx_soc = np.loadtxt('ImSHG_122_soc.dat')
# ax1.plot(openmx_soc[:,0], openmx_soc[:,1], label='openmx_soc')
# openmx_nsoc = np.loadtxt('ImSHG_122_nsoc.dat')
# ax1.plot(openmx_nsoc[:,0], 2*openmx_nsoc[:,1], label='2*openmx_nsoc')
epsilon='_e0.05'
abinit_soc = np.loadtxt('optic_2_0001_0002_0002-ChiTotIm_soc'+epsilon+'.out')
ax1.plot(abinit_soc[:,0], abinit_soc[:,2], label='abinit_soc')
abinit_nsoc = np.loadtxt('optic_2_0001_0002_0002-ChiTotIm_nsoc'+epsilon+'.out')
ax1.plot(abinit_nsoc[:,0], 2*abinit_nsoc[:,2], label='2*abinit_nsoc')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im SHG 122')
ax1.legend()
plt.xlim(0,6)
plt.title('1L-GeS Im_SHG_122')

ax2 = plt.subplot(122)
# openmx_soc = np.loadtxt('ReSHG_122_soc.dat')
# ax2.plot(openmx_soc[:,0], openmx_soc[:,1], label='openmx_soc')
# openmx_nsoc = np.loadtxt('ReSHG_122_nsoc.dat')
# ax2.plot(openmx_nsoc[:,0], 2*openmx_nsoc[:,1], label='2*openmx_nsoc')

abinit_soc = np.loadtxt('optic_2_0001_0002_0002-ChiTotRe_soc'+epsilon+'.out')
ax2.plot(abinit_soc[:,0], abinit_soc[:,2], label='abinit_soc')
abinit_nsoc = np.loadtxt('optic_2_0001_0002_0002-ChiTotRe_nsoc'+epsilon+'.out')
ax2.plot(abinit_nsoc[:,0], 2*abinit_nsoc[:,2], label='2*abinit_nsoc')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Re SHG 122')
ax2.legend()
plt.xlim(0,6)
# plt.ylim(-300,300)
plt.title('1L-GeS Re_SHG_122')
ax2.legend()
plt.tight_layout()
# plt.savefig('SHG_122_openmx_rescale.png')
plt.savefig('SHG_122_abinit'+epsilon+'_rescale.png')
# %%

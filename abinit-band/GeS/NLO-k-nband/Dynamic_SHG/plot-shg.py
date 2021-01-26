#%%
import matplotlib.pyplot as plt
import numpy as np

a='_4980_e0.02'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
openmx = np.loadtxt('ImSHG_122.dat')
ax1.plot(openmx[:,0], 2*openmx[:,1], label='openmx')
# abinit = np.loadtxt('ImSHG_111.dat')
abinit = np.loadtxt('optic_2_0001_0002_0002-ChiTotIm'+a+'.out')
ax1.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im SHG 122')
ax1.legend()
plt.xlim(0,6)
plt.title('1L-GeS Im_SHG_122')
ax2 = plt.subplot(122)
openmx = np.loadtxt('ReSHG_122.dat')
ax2.plot(openmx[:,0], 2*openmx[:,1], label='openmx')
# abinit = np.loadtxt('ReSHG_111.dat')
abinit = np.loadtxt('optic_2_0001_0002_0002-ChiTotRe'+a+'.out')
ax2.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('$\chi$$^{(2)}$$_{122}$')
ax2.legend()
plt.xlim(0,6)
# plt.ylim(-300,300)
plt.title('1L-GeS Re_SHG_122')
ax2.legend()
plt.tight_layout()
plt.savefig('SHG_122'+a+'_rescale.png')
# %%

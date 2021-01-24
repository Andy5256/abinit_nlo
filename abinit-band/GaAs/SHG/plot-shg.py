#%%
import matplotlib.pyplot as plt
import numpy as np

# a='_tol0.0002'
a='_2080'
plt.figure(figsize=(10,4), dpi=100)
plt.figure(1)
ax1 = plt.subplot(121)
openmx = np.loadtxt('ImSHG_123_k50.dat')
ax1.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ImSHG_111.dat')
abinit = np.loadtxt('optic_2_0001_0002_0003-ChiTotIm'+a+'.out')
ax1.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('Im SHG 123')
# plt.ylim(-300,300)
ax1.legend()
plt.xlim(0,6)
plt.title('GaAs Im_SHG_123')
ax2 = plt.subplot(122)
openmx = np.loadtxt('ReSHG_123_k50.dat')
ax2.plot(openmx[:,0], openmx[:,1], label='openmx')
# abinit = np.loadtxt('ReSHG_111.dat')
abinit = np.loadtxt('optic_2_0001_0002_0003-ChiTotRe'+a+'.out')
ax2.plot(abinit[:,0], abinit[:,2], label='abinit')
plt.xlabel('$\omega$ (eV)')
plt.ylabel('$\chi$$^{(2)}$$_{123}$')
ax2.legend()
plt.xlim(0,6)
# plt.ylim(-300,300)
plt.title('GaAs Re_SHG_123')
ax2.legend()
plt.tight_layout()
plt.savefig('SHG_123'+a+'.png')
# %%

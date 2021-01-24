#%%
import matplotlib.pyplot as plt
import numpy as np

file_path_openmx = "/home/wangjz/works/3.GeS/abinit/2.nlo/1.s=0/3.domega0.01_tol0.02/1290/Im_chi_11.dat"
openmx_Im = np.loadtxt(file_path_openmx)
file_path_openmx = "/home/wangjz/works/3.GeS/abinit/2.nlo/1.s=0/3.domega0.01_tol0.02/1290/Re_chi_11.dat"
openmx_Re = np.loadtxt(file_path_openmx)

# load files from different dir
# plot five fig with different tolerance
for i in [0.001, 0.005, 0.01, 0.05, 0.1]:
    plt.figure(figsize=(10,4), dpi=100)
    plt.figure(1)
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    ax1.plot(openmx_Im[:,0], openmx_Im[:,1], label='openmx200k140bs_0.02')
    ax2.plot(openmx_Re[:,0], openmx_Re[:,1], label='openmx200k140bs_0.02')
    for j in [0.02, 0.05, 0.1]:
        file_path = ("/home/wangjz/works/3.GeS/abinit/2.nlo/1.s=0/3.domega0.01_tol0.02/1290/%s_%s/optic_2_0001_0001-linopt.out" %(i,j))
        abinit = np.loadtxt(file_path)
        ax1.plot(abinit[:599,0], abinit[:599,1], linewidth=1, linestyle='--', label='abinit' + str(i) + '_' + str(j))
        ax2.plot(abinit[599:1197,0], abinit[599:1197,1], linewidth=1, linestyle='--', label='abinit' + str(i) + '_' + str(j))
    ax1.set_xlabel('$\omega$ (eV)')
    ax1.set_ylabel('Im $\epsilon$${_r}$$^{xx}$')
    ax1.legend()
    ax2.set_xlabel('$\omega$ (eV)')
    ax2.set_ylabel('Re $\epsilon$${_r}$$^{xx}$')
    ax2.legend()
    plt.xlim(0,6)
    ax1.set_xlim(0,6)
    ax2.set_xlim(0,6)
    ax1.set_title('1L-GeS Im_chi_11')
    ax2.set_title('1L-GeS Re_chi_11')
    plt.tight_layout()
    plt.savefig('Chi_11_'+'tol_'+str(i)+'.png')
ax1.legend_ =None
ax2.legend_ =None
# %%

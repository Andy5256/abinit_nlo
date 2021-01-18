#%%
import matplotlib.pyplot as plt
import numpy as np

info = np.loadtxt('BAND.dat')
for line in info:
    if 'Band-Index' not in 
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:26:55 2016

@author: Stephan
"""

import numpy as np
import scipy.optimize as optimization

def gaus_fit(x, a, x0, c):
    '''
    function used to find fractal dimension on a fit with
    N; partickles vs Radius of gyration
    '''
    return a*np.exp((-(x-x0)**2)/(2*c**2))
    
peaks=[]
errors=[]
for distances in distancesTime:
    y,x = np.histogram(distances, bins=50)
    x=x[1:]
    #plt.scatter(x,y)
    fit = optimization.curve_fit(gaus_fit, x, y)
    peaks.append(fit[0][1])
    perr = np.sqrt(np.diag(fit[1]))
    errors.append(perr[1])
    
plt.figure()
plt.scatter([i*10*60 for i in range(0,80)], peaks)
plt.errorbar([i*10*60 for i in range(0,80)], peaks, yerr=errors, fmt=None)
plt.xlabel("Time (s)")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ylabel("Distance from center to center in "+r'$\mu$'+'m')
#
##%%
#plt.figure()
#plt.scatter(x,y, c='r', label="data")
#
#y=[gaus_fit(i, fit[0][0],fit[0][1],fit[0][2]) for i in x]
#plt.plot(x,y, c='b', label="fit")
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.xlabel("distance between particles in um")
#plt.ylabel("counts")
#mpl.rcParams.update({'font.size': 22})
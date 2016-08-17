# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:23:41 2016

@author: Stephan
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import decimal
import scipy.optimize as optimization

# Source http://stackoverflow.com/questions/21242011/most-efficient-way-to-calculate-radial-profile


location = "D:\\bachelorproject\\image july\\"

doList=[i for i in range(0,160,2)]
color=['b','g','r','c','m','y','k']*10
print(doList)
fractalDim=[]
fractalDimError=[]
colorID=0
for item in doList:


    # Load image
    image = np.load(location + 'image_' + str(item) + '.npy')

    # Init
    dictionary = {}
    binSize=2.0
    colorID+=1

    frames = [i for i in range(5,35)]
    radialAvarage=[]
    #plt.figure()
    for frame in frames:

        #Select 2D frame
        imageFrame = image[frame]

        # FFT image
        timage = np.fft.fft2(imageFrame)

        # Shift middle to center
        shiftImage = np.fft.fftshift(timage)

        # Remove imaganary numbers
        absImage=np.abs(shiftImage)




        def radial_profile(data, center):
            global yun,xun,r,tbin,nr
            # create a matrix from 0-len(image)
            yun, xun = np.indices((data.shape))
            r = np.sqrt((xun - center[0])**2 + (yun - center[1])**2)
            # make radiuses matrix where every index is the radius to the center
            r = r.astype(np.int)

            # total value of circle
            tbin = np.bincount(r.ravel(), data.ravel())
            # amount of pixels
            nr = np.bincount(r.ravel())
            radialprofile = tbin / nr
            return radialprofile

        img = absImage
        # center, radi = find_centroid(img)
        center, radi = (512, 512), 1
        rad = radial_profile(img, center)
        if(len(radialAvarage) == 0):
            for radItem in rad:
                radialAvarage.append(radItem)
        else:
            for i in range(0,len(rad)):
                radialAvarage[i]+=rad[i]

    fity=[]
    fitx=[i for i in range(170,250)]
    for y in radialAvarage[170:250]:
        fity.append(y)

    def fractal_fit(x, a, df):
        '''
        function used to find fractal dimension on a fit with
        N; partickles vs Radius of gyration
        '''
        return a*x**(-df)

    fit, error = optimization.curve_fit(fractal_fit, fitx, fity)
    fractalDim.append(fit[1])
    perr = np.sqrt(np.diag(error))
    fractalDimError.append(perr[1])

    plt.plot([i for i in range(0,len(radialAvarage))], radialAvarage,
              label="Time "+ str(round(item*5/60.0,1)) + " hours")
   # plt.plot(fitx, [fractal_fit(i,fit[0],fit[1]) for i in range(45,60)])
plt.legend()
mpl.rcParams.update({'font.size': 18})
plt.legend(loc='center left', bbox_to_anchor=(0.5, 0.85))
plt.ylabel("S(q)")
plt.xlabel("q")
plt.xscale('log')
plt.yscale('log')
##%%
#plt.figure()
#plt.errorbar([i*10*60 for i in range(0,len(fractalDim))], fractalDim, yerr=fractalDimError, fmt=None)
#plt.scatter([i*10*60 for i in range(0,len(fractalDim))], fractalDim)
#plt.ylabel("Fractal dimension")
#plt.xlabel('Time (s)')
#mpl.rcParams.update({'font.size': 18})
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:23:41 2016

@author: Stephan
"""

import numpy as np
import matplotlib.pyplot as plt


location = "E:\\Stephan Bachelorproject\\20160627_long_3045.mdb\\images overnight\\"

doList=[40]
color=['b','g','r','c','m','y','k']*10

plt.figure()
colorID=0
for item in doList:
  
    
    # Load image
    image = np.load(location + 'image_' + str(item) + '.npy') 
    
    # Init
    dictionary = {}
    binSize=2.0
    colorID+=1  
    
    frames = [i for i in range(5,35)]
    frames=[10]
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
            global x,y,r, ind, sr, sim ,ri, deltar, rind, nr, csim, tbin
            
            # first determine radii of all pixels
            y,x = np.indices((data.shape))
            
            # 2D plot of all radius from center
            r = np.sqrt((x-center[0])**2+(y-center[1])**2)
            
            
            ind = np.argsort(r.flat) # get sorted indices
            sr = r.flat[ind] # sorted radii
            sim = data.flat[ind] # image values sorted by radii
            ri = sr.astype(np.int32) # integer part of radii (bin size = 1)
            
            
            # determining distance between changes
            deltar = ri[1:] - ri[:-1] # assume all radii represented
            rind = np.where(deltar)[0] # location of changed radius
            nr = rind[1:] - rind[:-1] # number in radius bin
            
            csim = np.cumsum(sim, dtype=np.float64) # cumulative sum to figure out sums for each radii bin
            tbin = csim[rind[1:]] - csim[rind[:-1]] # sum for image values in radius bins
            
            # devide by amount if pixels per radia
            radialprofile = tbin/nr # the answer
            return radialprofile
        
        img = absImage
        # center, radi = find_centroid(img)
        center, radi = (512, 512), 7
        rad = radial_profile(img, center)
        
        plt.plot(rad[radi:])
        plt.xscale('log')
        plt.yscale('log')
        plt.show()        
        
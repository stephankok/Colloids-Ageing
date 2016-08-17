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
            y, x = np.indices((data.shape))
            r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
            r = r.astype(np.int)
        
            tbin = np.bincount(r.ravel(), data.ravel())
            nr = np.bincount(r.ravel())
            radialprofile = tbin / nr
            return radialprofile 
        
        img = absImage
        # center, radi = find_centroid(img)
        center, radi = (512, 512), 1
        rad = radial_profile(img, center)
        
        plt.plot([x for x in range(0,len(rad[radi:]))], rad[radi:])
        plt.ylabel("S(q)")
        plt.xlabel("q")
        plt.xscale('log')
        plt.yscale('log')
        plt.show()        
        
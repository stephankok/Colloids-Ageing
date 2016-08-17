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
    
    frames = [i for i in range(5,35,5)]
    for frame in frames:
        
        colorID+=1  
        #Select 2D frame
        imageFrame = image[frame]
        
        # FFT image
        timage = np.fft.fft2(imageFrame)
        
        # Shift middle to center
        shiftImage = np.fft.fftshift(timage)
        
        # Remove imaganary numbers
        absImage=np.sqrt(np.abs(shiftImage**2))
        
       # Will contain all radius with their values so radius of d={5:20.2352} with
        # 5 the radius from the center and 20.2352 the value
        dictionary = {}
        # Do the angular intergration
        length=len(absImage)
        binSize=2.0
        for x in range(0,length):
            for y in range(0,length):
                radius = np.sqrt((x-(length/2.0))**2 + (y-(length/2.0))**2)
    
                radius =  int(radius / binSize)
                # remove edges
                if(radius <= 512 / binSize and radius >= 1):
                    if radius in dictionary:
                        dictionary[radius]+=absImage[x][y]
                    else:
                        dictionary[radius]=absImage[x][y]
        # particle = 7 pixels    
        
        # make 2 lists from the dictionary
        radiusHist=[]
        valueHist=[]
        for key, val in dictionary.items():
            radiusHist.append((key*binSize))
            valueHist.append(val)
#        
#        # Fit the fractal dimensions
#        # !!!!!!!! HARD CODED radius LIMITS!!!!!!
#        fitx=[]
#        fity=[]
#        for i in range(0,len(radiusHist)):
#            radius = radiusHist[i]
#            if (radius > 118 and radius < 223):
#            #if (radius > 43 and radius < 55):
#               fitx.append(radius) 
#               fity.append(valueHist[i])
#        
#        import scipy.optimize as optimization
#        def fractal_fit(x, a, df):
#            '''
#            function used to find fractal dimension on a fit with
#            N; partickles vs Radius of gyration
#            '''
#            return a*x**(-df)
#        
#        # show
        #fit = optimization.curve_fit(fractal_fit, fitx, fity)
        plt.scatter(radiusHist,valueHist, label =str(item) + " " + str(frame), c=color[-colorID])
        plt.xscale("log")
        plt.yscale("log")
        #plt.plot([i for i in range(50,500)],[fractal_fit(i,fit[0][0],fit[0][1]) for i in range(50,500)], c=color[-colorID], label=str(fit[0][1]))
plt.ylabel("S(q)")
plt.xlabel("q")
plt.legend()
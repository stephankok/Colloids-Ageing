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
    colorID+=1    
    
    # Load image
    image = np.load(location + 'image_' + str(item) + '.npy') 
    
    #Select 2D frame
    imageFrame = image[20]
    
    # FFT image
    timage = np.fft.fft2(imageFrame,norm="ortho")
    
    # Shift middle to center
    shiftImage = np.fft.fftshift(timage)
    
    # Remove imaganary numbers
    absImage=np.abs(shiftImage)
    
   # Will contain all radius with their values so radius of d={5:20.2352} with
    # 5 the radius from the center and 20.2352 the value
    dictionary = {}
    # Do the angular intergration
    length=len(absImage)
    
    for x in range(0,length):
        for y in range(0,length):
            radius = np.sqrt((x-(length/2.0))**2 + (y-(length/2.0))**2)

            radiusBin =  (radius)
            # remove edges
            if(radiusBin <= 512 and radiusBin > 0.0):
                if radiusBin in dictionary:
                    dictionary[radiusBin]+=absImage[x][y]
                else:
                    dictionary[radiusBin]=absImage[x][y]
    particleSize = 7
    
    # make 2 lists from the dictionary
    radiusHist=[]
    valueHist=[]
    for key, val in dictionary.items():
        radiusHist.append(1024.0 /(key*7))
        valueHist.append(val)
    

    list1, list2 = zip(*sorted(zip(radiusHist, valueHist)))
    
#    index=0
#    i=0
#    first=True
#    binnedRad=[]
#    binnedVal=[]
#    while(list1[index] - (2/7) < 0):
#        if(first):
#            binnedRad.append(list1[i])
#            binnedVal.append(list2[i])
#        else:
#            binnedRad[index] += list1[i+j]
#            binnedVal[index] += list2[i+j]
#        i+=1
#        
    
    binnedRad=[]
    binnedVal=[]
    binDept=50
    index = 0
    for i in range(0,len(list1)-binDept, binDept):
        binnedRad.append(list1[i])
        binnedVal.append(list2[i])
        for j in range(1,binDept):
            binnedRad[index] += list1[i+j]
            binnedVal[index] += list2[i+j]
        binnedRad[index] = binnedRad[index] / binDept
        index+=1
        
#    binDept2=5
#    for i in range(int(len(list1) / 2)-binDept, len(list1) -binDept2, binDept2):
#        binnedRad.append(list1[i])
#        binnedVal.append(list2[i])
#        for j in range(1,binDept2):
#            binnedRad[index] += list1[i+j]
#            binnedVal[index] += list2[i+j]
#        binnedRad[index] = binnedRad[index] / binDept2
#        index+=1
#    # Fit the fractal dimensions
#    # !!!!!!!! HARD CODED radius LIMITS!!!!!!
#    fitx=[]
#    fity=[]
#    for i in range(0,len(radiusHist)):
#        radius = radiusHist[i]
#        if (radius > 118 and radius < 223):
#        #if (radius > 43 and radius < 55):
#           fitx.append(radius) 
#           fity.append(valueHist[i])
#    
#    import scipy.optimize as optimization
#    def fractal_fit(x, a, df):
#        '''
#        function used to find fractal dimension on a fit with
#        N; partickles vs Radius of gyration
#        '''
#        return a*x**(-df)
#    
    # show
    #fit = optimization.curve_fit(fractal_fit, fitx, fity)
    plt.scatter(binnedRad,binnedVal, label =str(item), c=color[-colorID])
plt.xscale("log")
plt.yscale("log")
#plt.plot([i for i in range(50,500)],[fractal_fit(i,fit[0][0],fit[0][1]) for i in range(50,500)], c=color[-colorID], label=str(fit[0][1]))
plt.ylabel("S(q)")
plt.xlabel("qr")
plt.legend()
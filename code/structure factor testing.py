# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:23:41 2016

@author: Stephan
"""

import numpy as np
import matplotlib.pyplot as plt


location = "E:\\Stephan Bachelorproject\\20160627_long_3045.mdb\\images overnight\\"

doList=[40]
colors=['b','g','r','c','m','y','k']*1000

fig = plt.gcf()
ax = fig.gca()
colorID=0
for item in doList:
    colorID+=1    
    
    # Load image
    image = np.load(location + 'image_' + str(item) + '.npy') 
    
    #Select 2D frame
    imageFrame = image[20]
    
    # FFT image
    timage = np.fft.fft2(imageFrame)
    
    # Shift middle to center
    shiftImage = np.fft.fftshift(timage)
    
    # Remove imaganary numbers
    absImage=np.log(np.abs(shiftImage**2))
    
    # Will contain all radius with their values so radius of d={5:20.2352} with
    # 5 the radius from the center and 20.2352 the value
    dictionary = {}
    # Do the angular intergration
    length=len(absImage)
    for x in range(0,length):
        for y in range(0,length):
            radius = np.sqrt((x-(length/2.0))**2 + (y-(length/2.0))**2)

            radius =  int(radius / 2)
            # remove edges
            if(radius <= 512/2 and radius >= 1):
                if radius in dictionary:
                    dictionary[radius]+=absImage[x][y]
                else:
                    dictionary[radius]=absImage[x][y]

    # particle = 7 pixels    
    
    # make 2 lists from the dictionary
    radiusHist=[]
    valueHist=[]
    for key, val in dictionary.items():
        radiusHist.append((key*2))
        valueHist.append(val)
    
    
    for i in range(0,len(radiusHist),20):
        rad= radiusHist[i]
        circle = plt.Circle((512, 512), rad, color=colors[i],fill=False)
        ax.add_artist(circle) 

    
    plt.imshow(absImage)
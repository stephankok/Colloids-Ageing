# -*- coding: utf-8 -*-
"""
Created on Wed May  4 10:32:39 2016

@author: Stephan
"""

import pims
import matplotlib.pyplot as plt
import numpy as np
import trackpy as tp

# Load image
def load_image(location):
    print("Loading")
    frames = pims.Bioformats(location);
    print("finished loading")
    print("Resolution and Frames: ", frames.sizes)
    print(frames)
    return frames

def bandpass(image):  
    '''
    Firt do banpass then normalize.
    '''
    
    raw_frame = image.astype(float)
    
    bandpass = tp.bandpass(raw_frame,lshort=(2,2,1),llong=(10,10,3))
    
    # llong ~ particle diameter
    # lshort 1,2
    # lshort = (2,2,1)
    # llong = (10,10,3)

    return bandpass     

def normalize(image):
    int_max = image.max()
    int_min = image.min()
    
    image = (image - int_min) / (int_max - int_min)
    return image
            
    
def fractal_fit(x, df, a):
    '''
    function used to find fractal dimension on a fit with
    N; partickles vs Radius of gyration
    '''
    return np.power(x / a ,df)        
    
def main(image):     
    image = bandpass(image)
    image = normalize(image)
    return image


  
location = 'D:\\bachelorproject\\image july\\'
#location = "E:\\Stephan Bachelorproject\\20160627_long_3045.mdb\\images overnight\\"
#frames = load_image("E:\Stephan Bachelorproject\\20160627_long_3045.mdb\\stephan28overnight.lsm")
frames = load_image('C:\\Users\\Stephan\\Desktop\\Bachelorproject\\20160606_mg_4_4_2.mdb\\31deg_long_measure_0906.lsm')
i = 12
for frame in frames[12:60]:
    image = main(frame)
    np.save((location + 'image_' + str(i) + '.npy'), image)
    i += 1
    
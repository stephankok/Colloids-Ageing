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
    return frames

def bandpass_normalize(image, frame_number):  
    '''
    Firt do banpass then normalize.
    '''
    
    raw_frame = frames[frame_number].astype(float)
    
    bandpass = tp.bandpass(raw_frame,lshort=1,llong=10)
    
    int_max = bandpass.max()
    int_min = bandpass.min()
    
    bandpass = (bandpass - int_min) / (int_max - int_min)

    return bandpass     
 

location = "D:\\Bachelorproject\\metingen\\04_25_LM_1500-2200.mdb\\"
file = "2504_LM_1500_2200.lsm"   
frames = load_image(location + file)
normalized = bandpass_normalize(frames, 0)

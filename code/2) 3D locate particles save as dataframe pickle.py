# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 14:32:04 2016

@author: Stephan
"""

import numpy as np
import trackpy as tp
location = 'D:\\bachelorproject\\image july\\'
saveloc = 'D:\\bachelorproject\\features july\\'

for i in range(91,120):
    image = np.load(location + 'image_' + str(i) + '.npy')
    
    features = tp.locate(image, diameter=(7, 7, 3), minmass = 0.0, 
                             noise_size=1,
                             smoothing_size=(5,5,4), preprocess=False, separation=(15,15,6))
    features.to_pickle(saveloc+ "features_" + str(i) + ".pkl")
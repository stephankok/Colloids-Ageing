# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:29:00 2016

@author: Stephan
"""

FEATURESLOC = "E:\\Stephan Bachelorproject\\20160627_long_3045.mdb\\features overnight\\"
saveloc = "E:\\Stephan Bachelorproject\\20160627_long_3045.mdb\\features overnight masscut\\"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

for item in range(79,80):
    plt.figure()
    features = pd.read_pickle(FEATURESLOC+'features_'+str(item)+'.pkl')
    
    rangeMax=features['mass'].max()
    
    plt.hist(features['mass'], bins = 200, alpha=0.9, range=(0,rangeMax)
    , label = 'Before mass cutoff')
    
    y, x = np.histogram(features['mass'], bins = 200)
    x=x[1:]
    
    temp = 0
    for i in range(0, len(y)):
        if(temp < y[i]):
            temp=y[i]
            tempAnswer=i
        
    counts=y[tempAnswer]
    for i in range(tempAnswer+1,len(x)):
        if(y[i] < counts):
            counts = y[i]
            massCutoff = x[i]
        else:
            break
    features2 = features[features['mass'] > massCutoff*0.8]
    
    plt.hist(features2['mass'], bins = 200, alpha=0.9, range=(0,rangeMax),
             label = 'After mass cutoff')
    #features2.to_pickle(saveloc+ "features_" + str(item) + ".pkl")

plt.legend()
plt.title("Mass distribution of found particles")
plt.xlabel("Mass")
plt.ylabel("Counts")
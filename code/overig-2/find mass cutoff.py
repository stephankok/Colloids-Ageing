# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:29:00 2016

@author: Stephan
"""

FEATURESLOC = "D:\\bachelorproject\\features july\\"
saveloc = "D:\\bachelorproject\\features mascut july\\"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
1
for item in range(0,180):
    plt.figure()
    features = pd.read_pickle(FEATURESLOC+'features_'+str(item)+'.pkl')
    
    rangeMax=features['mass'].max()
    
    plt.hist(features['mass'], bins = 100, alpha=0.9, range=(0,rangeMax)
    , label = 'Before mass cutoff')
    
    y, x = np.histogram(features['mass'], bins = 100)
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
        elif(counts < y[tempAnswer]/5):
            break
    features2 = features[features['mass'] > massCutoff*0.8]
    
    #plt.hist(features2['mass'], bins = 100, alpha=0.9, range=(0,rangeMax),
    #         label = 'After mass cutoff')
    features2.to_pickle(saveloc+ "features_" + str(item) + ".pkl")

plt.legend()
plt.title("Mass distribution of found particles")
plt.xlabel("Mass")
plt.ylabel("Counts")
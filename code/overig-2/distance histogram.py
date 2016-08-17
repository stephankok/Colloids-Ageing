# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:02:10 2016

@author: Stephan
"""


FEATURESLOC = FEATURESLOC = "D:\\bachelorproject\\features mascut july\\"

import pims
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import trackpy as tp
import pandas as pd
import math
import pickle

class particle_class():
    def __init__(self, Id, xpos, ypos, zpos):
        self.identity = Id
        self.posx = xpos
        self.posy = ypos
        self.posz = zpos
        self.neigbour_list = []
    def get_x(self):
        return self.posx
    def get_y(self):
        return self.posy
    def get_z(self):
        return self.posz
    def add_neigbour(self, neigbour):
        self.neigbour_list.append(neigbour)
    def get_neigbour(self):
        return self.neigbour_list
    def remove_neigbour(self, pos):
        self.neigbour_list.remove(pos)
    def get_id(self):
        return self.identity
        
# loop trough doList range
doList = [i for i in range(0,160,2)]
#doList=[159,0]
#doList.append(0)
#doList=[0,10,40,70]
print(doList)
distancesTime=[]
plt.figure()
for item in doList:
    print(item)
    # load located features
    features = pd.read_pickle(FEATURESLOC+'features_'+str(item)+'.pkl')   

#    # Rezise particles radius
    features['z'] = (features['z'])*0.6
    features['x'] = (features['x'] / 1024)*105.77
    features['y'] = (features['y'] / 1024)*105.77
    
    # define cutoff
    cutoff = 3.5 # micro meters

    # Create particles class
    particles = []
    p_id = 0
    for index, row in features.iterrows():
        newparticle = particle_class(p_id, row['x'], row['y'], row['z'])
        neigbours = saveList[item][p_id][1]
        for neigbour in neigbours:
            newparticle.add_neigbour(neigbour)
        p_id += 1
        particles.append(newparticle)
    
    
#    # remoce particles with an range of 1.3 bigger then nearest particle
#    # and those closer than 1.5 um
#    for p in particles:  
#        minDis = 3.5
#        for n in p.get_neigbour():
#            n = particles[n]
#            distance = math.sqrt(math.pow(p.get_x() - n.get_x(),2) + math.pow(p.get_y() - n.get_y(),2) + math.pow(p.get_z() - n.get_z(),2))
#            if(distance < minDis and distance > 1):
#                minDis = distance
#    
#        for nID in p.get_neigbour():
#            n = particles[nID]
#            distance = math.sqrt(math.pow(p.get_x() - n.get_x(),2) + math.pow(p.get_y() - n.get_y(),2) + math.pow(p.get_z() - n.get_z(),2))
#            if(distance > minDis*1.3 or distance < 1.5):
#                p.remove_neigbour(nID)
    
    # todo make hist
    distancesList=[]
    for p in particles:
        x=p.get_x()
        y=p.get_y()
        z=p.get_z()
        for n in p.get_neigbour():
            neigbour = particles[n]
            nx = neigbour.get_x()
            ny = neigbour.get_y()
            
            nz = neigbour.get_z()
            distance=math.sqrt((x-nx)**2 + (y-ny)**2 + (z-nz)**2)
            distancesList.append(distance)
    distancesTime.append(distancesList)
    distancesList=[dist for dist in distancesList]
    plt.hist(distancesList, bins = 60, label= "Time "+ str(round(item*5/60.0,1)) + " hours")
plt.xlabel("Distance from center to center in "+r'$\mu$'+'m')
plt.ylabel("Counts")
plt.legend(loc='center left', bbox_to_anchor=(0.0, 0.7))
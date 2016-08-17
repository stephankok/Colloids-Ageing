
FEATURESLOC = "D:\\bachelorproject\\features mascut july\\"

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
    def get_id(self):
        return self.identity


# In[ ]:

'''
Find connectivity through time
'''
# init
particlesFoundList = []
meanNeigbourList = []
maxNeigbourList = []
minNeigbourList = []
histList = []
saveList = []

# loop trough doList range
doList = [i for i in range(0,180)]
print(doList)
for item in doList:
    
    tempHistList = []
    # load located features
    features = pd.read_pickle(FEATURESLOC+'features_'+str(item)+'.pkl')   
    
    # add found to list
    particlesFound = len(features)
    particlesFoundList.append(particlesFound)

    # Rezise particles radius
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
        p_id += 1
        particles.append(newparticle)
    # calculate connectivity 
    total = 0
    Max = 0
    Min = 100
    total_dis = []
    
    # loop over all particles
    for particle in particles:      
        # first find all neigbours
        for neigbour in particles:  
            # dont add yourself as neibour
            if (neigbour.get_id() != particle.get_id()):            
                distance = (math.pow(particle.get_x() - neigbour.get_x(),2) + 
                            math.pow(particle.get_y() - neigbour.get_y(),2) + 
                            math.pow(particle.get_z() - neigbour.get_z(),2))
                
                # check if between cutoff
                if(math.sqrt(distance) < cutoff):
                    total_dis.append(math.sqrt(distance))
                    particle.add_neigbour(neigbour.get_id())
                    total+=1
        if (len(particle.get_neigbour()) > Max):
            Max = len(particle.get_neigbour())
        if (len(particle.get_neigbour()) < Min):
            Min = len(particle.get_neigbour())
                
    meanTotal = 0
    particlesSaveList = []
    for particle in particles:
        meanTotal += len(particle.get_neigbour())
        tempHistList.append(len(particle.get_neigbour()))
        particlesSaveList.append([particle.get_id(), particle.get_neigbour()])
        
    meanNeigbourList.append(meanTotal / particlesFound)
    maxNeigbourList.append(Max)
    minNeigbourList.append(Min)
    saveList.append(particlesSaveList)
    histList.append(tempHistList)
    

    

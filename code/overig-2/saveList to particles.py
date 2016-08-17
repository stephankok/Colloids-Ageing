# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:02:10 2016

@author: Stephan
"""


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
        
# loop trough doList range
doList = [i for i in range(150,151)]
print(doList)
for item in doList:
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

#%%

from mpl_toolkits.mplot3d import Axes3D
import random
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.pbaspect= [1.0, 1.0, 24/105]
xs = []
ys = []
zs = []

xm=[]
ym=[]
zm=[]
for p in particles:
    if (len(p.get_neigbour()) > 6):
       xm.append(p.get_x())
       ym.append(p.get_y())
       zm.append(p.get_z())
       for n in p.get_neigbour():
           n = particles[n]
           xs.append(n.get_x())
           ys.append(n.get_y())
           zs.append(n.get_z())
           distance = math.sqrt(math.pow(p.get_x() - n.get_x(),2) + 
                            math.pow(p.get_y() - n.get_y(),2) + 
                            math.pow(p.get_z() - n.get_z(),2))
           print(distance)
   
ax.scatter(xm,ym,zm, c= 'r')   
ax.scatter(xs, ys, zs)       
#random.choice(colors.cnames.keys())
ax.set_xlabel('x '+ r'$\mu$'+'m')
ax.set_ylabel('y '+ r'$\mu$'+'m')
ax.set_zlabel('z '+ r'$\mu$'+'m')
#ax.set_xlim(0,30)
#ax.set_ylim(75,105)
#ax.set_zlim(0,30)

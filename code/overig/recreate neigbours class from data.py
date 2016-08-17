# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:04:38 2016

@author: Stephan
"""

class new_particle_class():
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
        
import math

disList=[]
distanceList = []
plotList = []
newPList=[]
for p in particles:
    x = p.get_x()
    y = p.get_y()
    z = p.get_z()
    neigbours = len(p.get_neigbour())
    mindis = 10
    maxdis = 0
    for n in p.get_neigbour():
        n=particles[n]
        nx = n.get_x()
        ny = n.get_y()
        nz = n.get_z()
        distance = math.sqrt( (x-nx)**2 + (y-ny)**2 + (z-nz)**2)
        disList.append(distance)
        if(distance > maxdis):
            maxdis = distance
        if(distance < mindis):
            mindis = distance
            
            
    distanceList.append([mindis, maxdis])            
    if(maxdis > mindis):
        plotList.append(mindis/maxdis)
    
    newP = new_particle_class(p.get_id(),x,y,z)
    for neigbourId in p.get_neigbour():
        n=particles[neigbourId]
        nx = n.get_x()
        ny = n.get_y()
        nz = n.get_z()
        distance = math.sqrt( (x-nx)**2 + (y-ny)**2 + (z-nz)**2)
        if(distance < mindis*2):
            newP.add_neigbour(neigbourId)
        else:
            print('deleted ' + str(mindis))
            
    print(len(p.get_neigbour()), len(newP.get_neigbour()))
    
    newPList.append(newP)
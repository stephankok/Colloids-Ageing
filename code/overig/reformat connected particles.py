# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:42:38 2016

@author: Stephan
"""

from mpl_toolkits.mplot3d import Axes3D
import random
import matplotlib.pyplot as plt
import math

for attemps in range(0,25):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.pbaspect= [1.0, 1.0, 24/105]
    xs = []
    ys = []
    zs = []
    
    xm=[]
    ym=[]
    zm=[]
    
    xrm=[]
    yrm=[]
    zrm=[]
    prev=[]
    done=False
    
    p = particles[random.randint(0,len(particles)-1)]
    prev.append(p.get_id())
    xm.append(p.get_x())
    ym.append(p.get_y())
    zm.append(p.get_z())
    ax.text(p.get_x(), p.get_y(), p.get_z(), str(len(p.
    get_neigbour())), color='red')
    
    minDis = 3.5
    for n in p.get_neigbour():
            n = particles[n]
            distance = math.sqrt(math.pow(p.get_x() - n.get_x(),2) + math.pow(p.get_y() - n.get_y(),2) + math.pow(p.get_z() - n.get_z(),2))
            if(distance< minDis and distance > 1):
                minDis = distance
    
    for n in p.get_neigbour():
        if n not in prev:
            prev.append(n)
            n = particles[n]
            distance = math.sqrt(math.pow(p.get_x() - n.get_x(),2) + math.pow(p.get_y() - n.get_y(),2) + math.pow(p.get_z() - n.get_z(),2))
            if(distance > minDis*1.3 or distance < 1):
                print("removed " + str(distance))
                xrm.append(n.get_x())
                yrm.append(n.get_y())
                zrm.append(n.get_z())
            else:
                xs.append(n.get_x())
                ys.append(n.get_y())
                zs.append(n.get_z())
     
     
    xo=[]
    yo=[]
    zo=[]   
    for p in particles:
        if (abs(xm[0] - p.get_x()) < 4.0 and abs(ym[0] - p.get_y()) < 4.0 and abs(zm[0] - p.get_z()) < 4.0):     
            if p.get_id() not in prev:
               xo.append(p.get_x())
               yo.append(p.get_y())
               zo.append(p.get_z())   
                   
    ax.scatter(xm,ym,zm, c= 'r', s=40)
    ax.scatter(xo,yo,zo, c= 'g', marker="+")   
    ax.scatter(xrm,yrm,zrm, c= 'b', marker="*")   
    ax.scatter(xs, ys, zs)  
    #random.choice(colors.cnames.keys())
    ax.set_xlabel('x '+ r'$\mu$'+'m')
    ax.set_ylabel('y '+ r'$\mu$'+'m')
    ax.set_zlabel('z '+ r'$\mu$'+'m')
    ax.set_xlim(xm[0]-5,xm[0]+5)
    ax.set_ylim(ym[0]-5,ym[0]+5)
    ax.set_zlim(zm[0]-5,zm[0]+5)
    print("done")
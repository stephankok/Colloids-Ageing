# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 14:10:36 2016

@author: Stephan
"""

import sys
sys.setrecursionlimit(10**6)

def search(neigbours, xs, ys, zs):
    global prev
    global midx
    global midy
    global midz
    #print(neigbours)
    if(len(neigbours) > 0):
        for nID in neigbours:
            if nID not in prev:
                n = particles[nID]
                xs.append(n.get_x())
                ys.append(n.get_y())
                zs.append(n.get_z())
                prev.append(n.get_id())
                search(n.get_neigbour(), xs, ys, zs)
                    


from mpl_toolkits.mplot3d import Axes3D
import random
import matplotlib.pyplot as plt
colour = ['b','g','r','c', 'm','y','k','w']
filled_markers = ['.','+','*','o','<','>','s','p','d']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100

prev = [0]
xs = []
ys = []
zs = []
search(particles[0].get_neigbour(), xs, ys, zs)
run = 0
for p in particles:
    if p.get_id() not in prev:
       if(run < 10) :
           run +=1
       else:
            xs = []
            ys = []
            zs = []
            prev.append(p.get_id())
    
            xs.append(p.get_x())
            ys.append(p.get_y())
            zs.append(p.get_z())
            search(p.get_neigbour(), xs, ys, zs)
            ax.scatter(xs, ys, zs, s=20, c='b')
            break
        
#random.choice(colors.cnames.keys())
ax.pbaspect = [1.0, 1.0, 105.77 / 20]
ax.set_xlabel('x '+ r'$\mu$'+'m')
ax.set_ylabel('y '+ r'$\mu$'+'m')
ax.set_zlabel('z '+ r'$\mu$'+'m')
ax.set_xlim(0,30)
ax.set_ylim(75,105)
ax.set_zlim(0,30)
plt.title("3D cluster of tracked particles")
print("done")
plt.show()
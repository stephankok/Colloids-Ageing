# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:24:20 2016

@author: Stephan
"""

'''
plot all clusters
'''
import sys
sys.setrecursionlimit(10**6)

def search(neigbours, xs, ys, zs):
    global prev
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

prev = []
for p in particles:
    if p.get_id() not in prev:
        xs = []
        ys = []
        zs = []
        prev.append(p.get_id())

        xs.append(p.get_x())
        ys.append(p.get_y())
        
        zs.append(p.get_z())
        search(p.get_neigbour(), xs, ys, zs)
        ax.scatter(xs, ys, zs, s=20, c=colour[random.randint(0,len(colour)-1)],
                   marker = filled_markers[random.randint(0,len(filled_markers)-1)])
        
#random.choice(colors.cnames.keys())
ax.pbaspect = [1.0, 1.0, 24/105]
ax.set_xlabel('x '+ r'$\mu$'+'m')
ax.set_ylabel('y '+ r'$\mu$'+'m')
ax.set_zlabel('z '+ r'$\mu$'+'m')
#ax.set_xlim(0,30)
#ax.set_ylim(75,105)
#ax.set_zlim(0,30)
plt.title("3D clusters of tracked particles")
print("done")
plt.show()
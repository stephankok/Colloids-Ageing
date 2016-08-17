# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:21:32 2016

@author: Stephan
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

colour = ['b','g','r','c', 'm','y','k','w']*100
filled_markers = ['.','+','*','o','<','>','s','p','d']*100

#i = 0
#y, x = np.histogram(histList[i], max(histList[i]))
#x = x[1:]
#plt.scatter(x,y)
#
#plt.figure()
#plt.plot(particlesFoundList)
#plt.title("amount of particles")
#
#plt.figure()
#plt.plot(meanNeigbourList)
#plt.title("meanNeigbours")
#
#plt.figure()
#plt.plot(maxNeigbourList)
#plt.title("maxNeigbours")
#
#
#plt.figure()
#newNeigbourList=[]
#for i in range(0,len(meanNeigbourList)):
#    newNeigbourList.append(meanNeigbourList[i]/particlesFoundList[i])
#plt.plot(newNeigbourList)
#plt.title("mean particles devided by all particles")
#plt.figure()
#
#doList = [0,1,10,11,25,26]
#for i in doList:
#    y, x = np.histogram(histList[i], 
#                        max(histList[i]))
#    x = x[1:]
#    plt.scatter(x,y, c=colour[i],marker=filled_markers[i], label=str(i))
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []
list8 = []
list9 = []
list10 = []
list11 = []
list12 = []
list13 = []
for i in range(0,len(histList)-1,2):
    y, x = np.histogram(histList[i], max(histList[i]))
    newy = []
    for yvalue in y:
        # put it in precentage form
        newy.append(yvalue*50 / particlesFoundList[i])
    y = newy
    
    y2, x2 = np.histogram(histList[i+1], max(histList[i+1]))
    newy2 = []
    for yvalue in y2:
        # put it in precentage form
        newy2.append(yvalue*50 / particlesFoundList[i+1])
    y2 = newy2
    
    list1.append(y[0]+y2[0])
    list2.append(y[1]+y2[1])
    list3.append(y[2]+y2[2])
    list4.append(y[3]+y2[3])
    list5.append(y[4]+y2[4])
    list6.append(y[5]+y2[5])
    list7.append(y[6]+y2[6])
    list8.append(y[7]+y2[7])
    list9.append(y[8]+y2[8])
#    list10.append(y[10])
#    list11.append(y[11])
#    list12.append(y[12])
#    list13.append(y[13])
xlist=[i*10*60 for i in range(0,80,2)]
plt.figure()

#plt.scatter(xlist,list1, label = "1 neigbours", c=colour[0], marker = filled_markers[0])
#plt.scatter(xlist,list2, label = "2 neigbours", c='r', marker = filled_markers[1])
plt.scatter(xlist,list3, label = "3 bonds", c='m', marker = '+')
plt.scatter(xlist,list4, label = "4 bonds", c='b', marker = filled_markers[3])
plt.scatter(xlist,list5, label = "5 bonds", c='g', marker = filled_markers[4])
#plt.scatter(xlist,list6, label = "6 neigbours", c=colour[5], marker = filled_markers[5])
plt.scatter(xlist,list7, label = "7 bonds", c='y', marker = filled_markers[6])
plt.scatter(xlist,list8, label = "8 bonds", c='b', marker = filled_markers[7])
plt.scatter(xlist,list9, label = "9 bonds", c='r', marker = filled_markers[8])
#plt.plot(list9, label = "9 neigbours")
#plt.plot(list10, label = "10 neigbours")
#plt.plot(list11, label = "11 neigbours")
#plt.plot(list12, label = "12 neigbours")
#plt.plot(list13, label = "13 neigbours")
plt.legend(loc='center left', bbox_to_anchor=(0.85, 0.5))
plt.title("Connectivity")
plt.ylabel("Particle count (percentage of total)")
plt.xlabel("Time (s)")
plt.ylim(-1,25)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
matplotlib.rcParams.update({'font.size': 22})


#
##smaller4=[]
##bigger4=[]
##for i in range(0,len(list1)):
##    smaller4.append(list1[i]+list2[i]+list3[i])
##    bigger4.append(list4[i]+list5[i])
#
#
##smaller4=[]
##bigger4=[]
##for i in range(0,len(list1)):
##    smaller4.append(list1[i]+list2[i]+list3[i]+list4[i])
##    bigger4.append(list5[i]+list6[i]+list7[i]+list8[i]+list9[i])
#
#
#smaller4=[]
#bigger4=[]
#for i in range(0,len(list1)):
#    smaller4.append(list1[i]+list2[i])
#    bigger4.append(list3[i]+list4[i]+ list5[i]+list6[i]+list7[i])
#
#
#plt.figure()
#xlist=[i*10 for i in range(0,len(list1))]
#plt.scatter(xlist,smaller4, c='r',marker="*", label="2 neigbours and less")
#plt.scatter(xlist,bigger4, c='b',marker="+", label="3 neigbours and more")
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.xlabel("time in minuts")
#plt.ylabel("% of total particles")
#
#
#
#
#
#
#plt.figure()
#
#doList = [0,5,35,69, 74]
#for i in doList:
#    y, x = np.histogram(histList[i]+histList[i+1]+histList[i+2]+histList[i+3]+histList[i+4], 
#                        max(histList[i]+histList[i+1]+histList[i+2]+histList[i+3]+histList[i+4]))
#    x = x[1:]
#    plt.scatter(x,y, c=colour[i],marker=filled_markers[i], label=str(i))
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#
#
#list2 = []
#list3 = []
#list4 = []
#list5 = []
#list6 = []
#list7 = []
#list8 = []
#list9 = []
#list10 = []
#list11 = []
#list12 = []
#list13 = []
#for i in range(0,len(histList)):
#    y, x = np.histogram(histList[i], max(histList[i]))
#    newy = []
#    for yvalue in y:
#        newy.append(yvalue)
#    y = newy
#    x = x[1:]
#    list2.append(y[2])
#    list3.append(y[3])
#    list4.append(y[4])
#    list5.append(y[5])
##    list6.append(y[6])
##    list7.append(y[7])
##    list8.append(y[8])
##    list9.append(y[9])
##    list10.append(y[10])
##    list11.append(y[11])
##    list12.append(y[12])
##    list13.append(y[13])
#    
#plt.figure()
#plt.plot(list2, label = "2 neigbours")
#plt.plot(list3, label = "3 neigbours")
#plt.plot(list4, label = "4 neigbours")
#plt.plot(list5, label = "5 neigbours")
##plt.plot(list6, label = "6 neigbours")
##plt.plot(list7, label = "7 neigbours")
##plt.plot(list8, label = "8 neigbours")
##plt.plot(list9, label = "9 neigbours")
##plt.plot(list10, label = "10 neigbours")
##plt.plot(list11, label = "11 neigbours")
##plt.plot(list12, label = "12 neigbours")
##plt.plot(list13, label = "13 neigbours")
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.title("Neigbours in time")
#plt.ylabel("Amount of particles with # amount of neigbours")
#plt.xlabel("time in 10 minuts")

# coding: utf-8

# In[4]:

import pims
import matplotlib.pyplot as plt
import numpy as np
import trackpy as tp
import scipy.optimize as optimization
import pandas as pd
#saveloc = "D:\\bachelorproject\\newfeatures\\"
saveloc = "E:\\Stephan Bachelorproject\\20160627_long_3045.mdb\\features overnight\\"


# In[58]:


"""
Created on Wed May  4 10:32:39 2016

@author: Stephan
"""

def center_of_mass(particles):
    '''
    Calculate the center of mass
    All particles have same weigth
    '''
    total_x = 0
    total_y = 0
    total_z = 0
    count = 0
    for index, row in particles.iterrows():
        total_x += row['x']
        total_y += row['y']
        total_z += row['z']
        count += 1 
    cm_x = total_x / count
    cm_y = total_y / count
    cm_z = total_z / count
    return cm_x, cm_y, cm_z
    
def radius_of_gyration(particles, cm_x, cm_y, cm_z):   
    '''
    Calculate radius of gyration as
    Rg = sqrt(N / sum(r))
    with Rg: radius of gyration
    N: amount of particles
    r: distance to center of mass
    '''
    # calculate mean distance
    total_sum = 0
    count = 0
    for index, row in particles.iterrows():
        x = row['x'] 
        y = row['y']
        z = row['z']
        count += 1
        total_sum += (np.sqrt(x**2 + y**2 + z**2) - np.sqrt(cm_x**2 + cm_y**2 + cm_z**2))**2
    Rg = np.sqrt(total_sum / count)
    return Rg, count 
 
def particles_within(particles, radius, ofsetx, ofsety, ofsetz):
    '''
    Make a circle and find the particles that are inside this circle.
    '''
    return particles[( ((radius + ofsetx - particles['x'])**2 + (radius + ofsetz - particles['z'])**2 +
            (radius + ofsety - particles['y'])**2) < radius**2 )]
            
    
def fractal_fit(x, df, a):
    '''
    function used to find fractal dimension on a fit with
    N; partickles vs Radius of gyration
    '''
    return np.power(x / a ,df)        
    
def main(frameNumber): 
    global pfound  
    global Rgs
    global Ns
    
    features = pd.read_pickle(saveloc+ "features_" + str(frameNumber) + ".pkl")
    
    histList = plt.hist(features['mass'], bins = 1000)
    countList = histList[0]
    massList = histList[1]

    lowest = len(features)
    massMinimum = 0
    for i in range(0,len(countList)):
        # check for upper lowest bound???
        if(countList[i] < lowest):
            lowest = countList[i]
            massMinimum = massList[i]
    
    features = features[features['mass'] > (massMinimum*0.7)]
    plt.clf()
    
    #print("Rezise particles radius")
    features['z'] = (features['z'])*0.6
    features['x'] = (features['x'] / 1024)*105.77
    features['y'] = (features['y'] / 1024)*105.77        
        
    #update
    #print("found " + str(len(features)) + " paricles!")
    pfound.append(len(features))

    max_radius = int(40*0.6) # Edit this to max z heigth of measurement
    
    for rad in range(max_radius, 3,-1):
        for width in range(-105,105,20):     
            ofsetx = max_radius - rad - width#+ ofset_x_start
            ofsety = max_radius - rad - width#+ ofset_y_start
            ofsetz = max_radius - rad
            # in 3d
            particles_in_rad = particles_within(features, rad, ofsetx, ofsety, ofsetz)
 
            if(particles_in_rad.empty == False):
                
                # calculate center of mass
                cm_x, cm_y, cm_z = center_of_mass(particles_in_rad)
                
                # calculate mean distance
                Rg, N = radius_of_gyration(particles_in_rad, cm_x, cm_y, cm_z)  
            
                if(N > 2):
                    # only when more then 10 particles
                    Rgs.append(Rg)
                    Ns.append(N) 
                    



# In[59]:

def fractal_fit(x, df, a):
    '''
    function used to find fractal dimension on a fit with
    N; partickles vs Radius of gyration
    '''
    return np.power(x / a ,df)

pfound = []
fits = []
foundFractalDim = []
RvsN = []

for frameNumber in range(30,80):
    Rgs = []
    Ns = []
    main(frameNumber)
    fit = optimization.curve_fit(fractal_fit, Rgs, Ns)
    fits.append(fit)
    RvsN.append([Rgs, Ns, fit[0][0]])
    foundFractalDim.append(fit[0][0])

plt.clf()
plt.figure()
for Rgs, Ns, Df in RvsN:
    plt.scatter(Rgs, Ns, label = str(Df), c=np.random.rand(3,1))
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()


# In[39]:

print(pfound)
print(fit)


# In[43]:

plt.figure()
plt.scatter(Rgs,Ns)
plt.xscale("log")
plt.yscale('log')
plt.show()


# In[50]:

plt.figure()
plt.plot(foundFractalDim)
plt.show()


# In[41]:

plt.figure()
plt.plot(pfound)
plt.show()


# In[ ]:




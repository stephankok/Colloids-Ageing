# -*- coding: utf-8 -*-
"""
Created on Wed May  4 10:32:39 2016

@author: Stephan
"""

import pims
import matplotlib.pyplot as plt
import numpy as np
import trackpy as tp
import scipy.optimize as optimization

# Load image
def load_image(location):
    print("Loading")
    frames = pims.Bioformats(location);
    print("finished loading")
    print("Resolution and Frames: ", frames.sizes)
    return frames

def bandpass(image):  
    '''
    Firt do banpass then normalize.
    '''
    
    raw_frame = image.astype(float)
    
    bandpass = tp.bandpass(raw_frame,lshort=1,llong=10)

    return bandpass     

def normalize(image):
    int_max = image.max()
    int_min = image.min()
    
    image = (image - int_min) / (int_max - int_min)
    return image


def center_of_mass(particles):
    '''
    Calculate the center of mass
    All particles have same weigth
    '''
    total_x = 0
    total_y = 0
    count = 0
    for index, row in particles.iterrows():
        total_x += row['x']
        total_y += row['y']
        count += 1
    
    cm_x = total_x / count
    cm_y = total_y / count
    
    #print("Center of mass: ", cm_x, ", ", cm_y)
    #print("center of mass:" + str(cm_x) +  "," + str(cm_y))
    return cm_x, cm_y
    
def radius_of_gyration(particles, cm_x, cm_y):   
    '''
    Calculate radius of gyration as
    Rg =  1 / N * sum(r)
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
        count += 1
        
        total_sum += np.sqrt((x - cm_x)**2 + (y - cm_y)**2)
    
    Rg = (total_sum / count)
    #print("radius_of_gyration", str(Rg))
    return Rg, count 
 
def particles_within(particles, radius, ofset_x = 0, ofset_y = 0):
    '''
    Make a circle and find the particles that are inside this circle.
    '''
    #print("offset" + str(ofset_x) + "," + str(ofset_y))
    return particles[( ((radius + ofset_x - particles['x'])**2 + 
            (radius + ofset_y - particles['y'])**2) < radius**2 )]
            
    
def fractal_fit(x, df, a):
    '''
    function used to find fractal dimension on a fit with
    N; partickles vs Radius of gyration
    '''
    return np.power(x / a ,df)        
    
def main(image, do_bandpass = True, do_normalize = True, no_imj = False): 
    
    Rgs = []
    Ns = []
    # preprocess
    if(do_bandpass):
        print("bandpass")
        image = bandpass(image)
        
        
    if(do_normalize):
        print("normalize")
        image = normalize(image)
        #locate
        if(no_imj):
            print("no imageJ")
            particles = tp.locate(image,11, minmass  = 2, maxsize = 16, separation = 8)
        else:
            particles = tp.locate(image, 21, minmass = 15)

    else:
        #locate
        particles = tp.locate(image,11, minmass  = 6870, maxsize = 16, separation = 8)
        
        
    #update
    print("found " + str(len(particles)) + " paricles!")
    pfound.append(len(particles))
    
    mean_size = particles['size'].mean()
 
    #print(mean_size)
    # Make a big circle and go smaller and smaller
    '''
    middle = particles[particles['x'] > 462]
    middle = middle[middle['x'] < 562]
    #print(middle)
    
    middle = middle[middle['y'] > 462]
    middle = middle[middle['y'] < 562]
    #print(middle)
    for index, row in middle.iterrows():
        x = row['x'] 
        y = row['y']
        break
    if(x < int(len(image) / 2) or y < int(len(image) / 2) ):
        if( x < y):
            max_radius = int(x)
            ofset_y_start = int(len(image) - y)
            ofset_x_start = 0
        else:
            max_radius = int(y)
            ofset_x_start = int(len(image) - x)
            ofset_y_start = 0
    else:
        if( x > y):
            max_radius = int(x)
            ofset_y_start = int(len(image) - y)
            ofset_x_start = int(len(image) / 2)
        else:
            max_radius = int(y)
            ofset_x_start = int(len(image) - x)
            ofset_y_start = int(len(image) / 2)
           ''' 
    max_radius = int(len(image) / 2)
    for rad in range(max_radius, 1,-5):
        ofsetx = max_radius - rad #+ ofset_x_start
        ofsety = max_radius - rad #+ ofset_y_start
        particles_in_rad = particles_within(particles, rad, ofset_x = ofsetx, ofset_y = ofsety)
        
        
        
        if(particles_in_rad.empty == False):
            
            # calculate center of mass
            cm_x, cm_y = center_of_mass(particles_in_rad)
            
            # calculate mean distance
            Rg, N = radius_of_gyration(particles_in_rad, cm_x, cm_y)  
        
    
            if(N > 2):
                #print(np.log(N) / np.log(Rg / mean_size))
                Rgs.append(Rg)
                Ns.append(N)      

    return (particles,mean_size, Rgs, Ns)
 
    
import pandas as pd    
    
def check():
    '''
    used to check if code works.
    '''
    heigth = 5000
    width = heigth
    distance_between_particles_cores = 20
    
    global x_list
    global y_list
    global data
    global Rgs, Ns
    Rgs = []
    Ns = []

    x_list = []
    y_list = []
    print("build coords")
    for x in range(0, width, distance_between_particles_cores):
        for y in range(0, heigth, distance_between_particles_cores):
            x_list.append(x)
            y_list.append(y)

    d = {'x' : x_list,'y' : y_list}
    data = pd.DataFrame(d)

    print("done")
    
    
    max_radius = int(heigth / 2)
    for rad in range(max_radius, 1,-100):
        print(rad)
        ofsetx = max_radius - rad
        ofsety = max_radius - rad
        particles_in_rad = particles_within(data, rad, ofset_x = ofsetx, ofset_y = ofsety)
        
        
        
        if(particles_in_rad.empty == False):
            
            # calculate center of mass
            cm_x, cm_y = center_of_mass(particles_in_rad)
            
            # calculate mean distance
            Rg, N = radius_of_gyration(particles_in_rad, cm_x, cm_y)  
        
    
            if(N > 200):
                #print(np.log(N) / np.log(Rg / mean_size))
                Rgs.append(Rg)
                Ns.append(N)    
    
    
    print("finished")
    
    



location = "D:\\Bachelorproject\\metingen\\04_25_LM_1500-2200.mdb\\"
file = "2504_LM_1500_2200.lsm"   
frames = load_image(location + file)

Rgs = []
Rgs_per_frame = []
Ns = []
Ns_per_frame  = []
fit_fracts = []
run = 0
global pfound
pfound = []
for frame in frames:
    global meansize
    print("next run", run)
    run+=1
    particles, meansize, rg, n = main(frame, no_imj = True)
    #tp.annotate(particles, frame)

    Rgs_per_frame.append(rg)
    Ns_per_frame.append(n)
    for i in range(len(rg)):
        Rgs.append(rg[i])
        Ns.append(n[i])

    fit = optimization.curve_fit(fractal_fit, rg, n, [1.5, 15])
    fit_fracts.append(fit[0][0]) 

    

#%%

fit = optimization.curve_fit(fractal_fit, Rgs, Ns, [1.5, 15])
print(fit)
plt.figure()
plt.title("Rg vs N df: " + str(fit[0][0]))
plt.xlabel("Radius of gyration")
plt.ylabel("particles")
plt.scatter(Rgs, Ns)
x_list = np.arange(10,500)
y_list = [fractal_fit(x, fit[0][0], fit[0][1]) for x in x_list]
plt.plot(x_list, y_list)
plt.xscale('log')
plt.yscale('log')



#%%
'''
image = normalize(bandpass(frames[399]))
image1 = normalize((frames[399]))
particles = tp.locate(image,11, minmass  = 2, maxsize = 16, separation = 8)
particles1 = tp.locate(image1,11, minmass  = 2, maxsize = 16, separation = 8)
plt.figure()
tp.annotate(particles, image)
plt.show()
plt.figure()
tp.annotate(particles1, image)
plt.show()
'''

#%%
'''
image = normalize(bandpass(frames[0]))
image1 = normalize(bandpass(frames[1]))
particles = tp.locate(image,11, minmass  = 2, maxsize = 16, separation = 8)
particles1 = tp.locate(image1,11, minmass  = 2, maxsize = 16, separation = 8)
plt.figure()
plt.title("frame 0")
tp.annotate(particles, image)
plt.figure()
plt.title("")
tp.annotate(particles1, image1)
'''
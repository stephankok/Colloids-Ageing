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
        
        total_sum += np.sqrt((x - cm_x)**2) + np.sqrt((y - cm_y)**2)
    
    Rg = (total_sum / count)
    #print("radius_of_gyration", Rg)
    return Rg, count 
 
def particles_within(particles, radius, ofset_x = 0, ofset_y = 0):
    '''
    Make a circle and find the particles that are inside this circle.
    '''
    return particles[( ((radius + ofset_x - particles['x'])**2 + 
            (radius + ofset_y - particles['y'])**2) < radius**2 )]
            
            
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
            particles = tp.locate(image,11, minmass  = 5, maxsize = 16, seperation = 8)
        else:
            particles = tp.locate(image, 21, minmass = 15)

    else:
        #locate
        particles = tp.locate(image,11, minmass  = 6870, maxsize = 16, separation = 8)
        
        
    #update
    print("found " + str(len(particles)) + " paricles!")
    
    mean_size = particles['size'].mean()
    print(mean_size)
    # Make a big circle and go smaller and smaller
    max_radius = int(len(image) / 2)
    
    for rad in range(max_radius, 1,-5):
        ofsetx = rad - max_radius
        ofsety = rad - max_radius
        particles_in_rad = particles_within(particles, rad, ofsetx, ofsety)
        
        
        
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
        

def calculate_bandpass_normalized():
    location = "D:\\Bachelorproject\\metingen\\04_25_LM_1500-2200.mdb\\"
    file = "2504_LM_1500_2200 IMJ.lsm"   
    frames = load_image(location + file)
    
    Rgs = []
    Ns = []
    fit_fracts = []
    run = 0
    for frame in frames[200:201]:
        global meansize
        print("next run", run)
        run+=1
        particles, meansize, rg, n = main(frame)
        tp.annotate(particles, frame)
        '''
        for i in range(len(rg)):
        Rgs.append(rg[i])
        Ns.append(n[i])
    
        def fractal_fit(x, df, a):
            '''
        #function used to find fractal dimension on a fit with
        #N; partickles vs Radius of gyration
        '''
        return np.power(x / meansize ,df)
    
        fit = optimization.curve_fit(fractal_fit, rg, n, [1.5, 2.5])
        fit_fracts.append(fit[0][0])
        '''
#calculate_bandpass_normalized()

#%%
def calculate_bandpass_NOT_normalized():
    location = "D:\\Bachelorproject\\metingen\\04_25_LM_1500-2200.mdb\\"
    file = "2504_LM_1500_2200 IMJ.lsm"   
    frames = load_image(location + file)
    
    Rgs = []
    Ns = []
    fit_fracts = []
    run = 0
    for frame in frames[:420]:
        global meansize
        print("next run", run)
        run+=1
        particles, meansize, rg, n = main(frame, do_normalized = False)
        
        for i in range(len(rg)):
            Rgs.append(rg[i])
            Ns.append(n[i])
    
        def fractal_fit(x, df, a):
            '''
            function used to find fractal dimension on a fit with
            N; partickles vs Radius of gyration
            '''
            return np.power(x / meansize ,df)
    
        fit = optimization.curve_fit(fractal_fit, rg, n, [1.5, 2.5])
        fit_fracts.append(fit[0][0])
        

#Calculate banpass Not normalized of image NO imageJ
location = "D:\\Bachelorproject\\metingen\\04_25_LM_1500-2200.mdb\\"
file = "2504_LM_1500_2200.lsm"   
frames = load_image(location + file)

Rgs = []
Ns = []
fit_fracts = []
run = 0
for frame in frames[:10]:
    global meansize
    print("next run", run)
    run+=1
    particles, meansize, rg, n = main(frame, do_normalize = False)
    
    for i in range(len(rg)):
        Rgs.append(rg[i])
        Ns.append(n[i])

    def fractal_fit(x, df, a):
        '''
        function used to find fractal dimension on a fit with
        N; partickles vs Radius of gyration
        '''
        return np.power(x / a ,df)

    fit = optimization.curve_fit(fractal_fit, rg, n, [1.5, 2.5])
    fit_fracts.append(fit[0][0])  
   #tp.annotate(particles, frame)
    

#%%

x_list = np.arange(10,500)
y_list = [fractal_fit(x, fit[0][0], fit[0][1]) for x in x_list]

plt.scatter(Rgs, Ns)
plt.plot(x_list, y_list)
plt.title("Rg vs N df: " + str(fit[0][0]))
plt.xlabel("Radius of gyration")
plt.ylabel("particles")
plt.xscale('log')
plt.yscale('log')
plt.show()    

#%%
'''
plt.plot(fit_fracts)
plt.title("Fractal dimension Fitted func: (x / a)^Df")
plt.ylabel('fractal dimension')
plt.xlabel('frames in time 30s/frame')
plt.show()
'''
#%%
'''
fit = optimization.curve_fit(fractal_fit, Rgs, Ns, [1.5,3])
x_list = [x for x in range(0,500)]
y_list = [fractal_fit(x, fit[0][0], fit[0][1]) for x in x_list]
plt.scatter(Rgs, Ns)
plt.scatter(x_list, y_list, marker = '.', s = 40)
plt.title("Rgs and N of every frame together df: " + str(fit[0][0]))
plt.xlabel("Radius of gyration")
plt.yloval("Amount of particles")
plt.show()
'''

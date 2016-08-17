# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 11:20:43 2016

@author: Stephan
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:56:50 2016

@author: Stephan
"""

import pims
import matplotlib.pyplot as plt
import numpy as np

# Load image
def load_image(location):
    print("Loading")
    frames = pims.Bioformats(location);
    print("finished loading")
    print("Resolution and Frames: ", frames.sizes)
    return frames

'''
First collect the sum of all pixels per frame
'''
def intensity_per_pixel(frames, bits12=False):
    frames.iter_axes = 'z'
    frames_sum = []
    pixels = frames.frame_shape[0]*frames.frame_shape[1]
    
    z = len(frames)
    for i in range(z):
        if (i % 10 == 0):
            print("calculated frame: ", i + 1, "of ", z, " frames.")
        intensity = float(frames[i].sum()) / float(pixels)
        
        # if 12 bits ipv 8
        if(bits12):
            intensity = intensity * float(2**8) / float(2**12)
        frames_sum.append(intensity)
        
    return frames_sum
    
'''
Manipulate the found list so they start about the same place
'''
def manipulate(the_list):
    the_list = the_list[np.argmax(the_list):] # -5 because the top is not always the start of particles
    
    avarage = max(the_list)    
    #avarage = np.mean(the_list) # delete by avarage
    #avarage = the_list[0]      # they really start in the same point
    for i in range(len(the_list)):
        the_list[i] = the_list[i] - avarage
    return the_list

'''
imporved one
'''
def manipulate2(the_list, blanc_list):
    new_list = []
       
    for i in range(np.argmax(the_list), len(the_list)):
        try:
            avarage = blanc_list[i]
            new_list.append(the_list[i] - avarage)
        except:
            print("out of bound")
            
    return new_list
    
#%%
    
folder = "D:\\Bachelorproject\\metingen\\04_25_LM_1500-2200.mdb\\"    

'''
Files to read
'''
zstack1 = load_image(folder + "2504_LM_Zstack_1.lsm")
zstack2 = load_image(folder + "2504_LM_Zstack_31_75_2.lsm")
zstack3 = load_image(folder + "2504_LM_Zstack_30_75_before.lsm")
zstack4 = load_image(folder + "z_stack_after_LM_2604.lsm")
zstack5 = load_image(folder + "z_stack_after_LM_2604_laser3.lsm")

#%%

'''
Calculate intensitys
'''
int1 = intensity_per_pixel(zstack1)
int2 = intensity_per_pixel(zstack2)
int3 = intensity_per_pixel(zstack3)
int4 = intensity_per_pixel(zstack4)
int5 = intensity_per_pixel(zstack5)


#%%
'''
Plot Figure
'''
plt.figure()

plt.plot(int1, label = "When hit 31.75 degrees")
plt.plot(int2, label = "31.75 degrees after 5 min")
plt.plot(int3, label = "cooled down too 30.75 deg")
plt.plot(int4, label = "30.75 deg after 19 hours")
plt.plot(int5, label = "30.75 deg after 19 hours high laser power")

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("Intensity per pixel")
plt.xlabel("z level in \u00B5m")
plt.ylabel("Intensity per pixel")
plt.show()

#%%

man1 = manipulate(int1)
man2 = manipulate(int2)
man3 = manipulate(int3)
man4 = manipulate(int4)
man5 = manipulate(int5)

#%%
'''
Plot Figure
'''
plt.figure()

plt.plot(man1, label = "When hit 31.75 degrees")
plt.plot(man2, label = "31.75 degrees after 5 min")
plt.plot(man3, label = "cooled down too 30.75 deg")
plt.plot(man4, label = "30.75 deg after 19 hours")
plt.plot(man5, label = "30.75 deg after 19 hours high laser power")

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("Intensity per pixel")
plt.xlabel("z level in \u00B5m")
plt.ylabel("Intensity per pixel")
plt.show()
#%%
import scipy.optimize as optimization

def func(z, a, b):
    return np.exp(-z / b)
    
z_list = [i for i in range(len(man5))]
    
fit = optimization.curve_fit(func, z_list, man5)

y_list = [func(z, fit[0][0], fit[0][1]) for z in z_list]
print(fit[0])

plt.plot(man5)
plt.scatter(z_list, y_list)
plt.show()
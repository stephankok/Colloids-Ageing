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
    
frames = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_begin.lsm")

#%%

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
        
    plt.plot(frames_sum)
    plt.show()
    
    return frames_sum
    #%%    
        
begin = intensity_per_pixel(frames)

frames2 = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_gel1.lsm")
gel1 = intensity_per_pixel(frames2)

frames3 = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_afk1_pinhole_klein.lsm")
afgekoeld1 = intensity_per_pixel(frames3)

frames4 = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_gel2_32_before_measure_pinhole_klein.lsm")
gel2 = intensity_per_pixel(frames4)

frames5 = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_gel2_32_after_long_measure_pinhole_klein.lsm")
afterlongmeasure = intensity_per_pixel(frames5)
#%%
frames6 = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_gel2_33_pinhole_klein.lsm")
gel2_33 = intensity_per_pixel(frames6)

#%%
frames7 = load_image("D:\\Bachelorproject\\metingen\\04_22_longmeasure_27wt_30mM\\longmeasure_sk1504_27lut_30mM.mdb\\zstack_maandag.lsm")
maandag = intensity_per_pixel(frames7, bits12=True)

#%%

plt.figure()
plt.plot(begin, label = "begin, T=31")
plt.plot(gel1, label = "first time gel, T=33")
plt.plot(afgekoeld1, label = "afgekoeld (geen gel), T=31")
plt.plot(gel2_33, label = "tweede gel, T=33")
plt.plot(gel2, label = "Dezelfde gel (voor lange meting), T=32")
plt.plot(afterlongmeasure, label = "na lange meting, T=32")
plt.plot(maandag, label = "after 70u, T=32")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("27 wt lut 30mM geen verdunning")
plt.xlabel("z level in \u00B5m")
plt.ylabel("Intensity per pixel")
plt.show()

#%%
'''
Manipulate the found list so they start about the same place
'''
def manipulate(the_list):
    the_list = the_list[np.argmax(the_list)-5:] # -5 because the top is not always the start of particles
    
    avarage = max(the_list)    
    #avarage = np.mean(the_list) # delete by avarage
    #avarage = the_list[0]      # they really start in the same point
    for i in range(len(the_list)):
        the_list[i] = the_list[i] - avarage
    return the_list

begin1 = manipulate(begin)
gel11 = manipulate(gel1)
afgekoeld11 = manipulate(afgekoeld1)
gel21 = manipulate(gel2)
afterlongmeasure1 = manipulate(afterlongmeasure)
gel2_331 = manipulate(gel2_33)
maandag1 = manipulate(maandag)


plt.figure()
plt.plot(begin1, label = "begin, T=31")
plt.plot(gel11, label = "first time gel, T=33")
plt.plot(afgekoeld11, label = "afgekoeld (geen gel), T=31")
plt.plot(gel2_331, label = "tweede gel, T=33")
plt.plot(gel21, label = "Dezelfde gel (voor lange meting), T=32")
plt.plot(afterlongmeasure1, label = "na lange meting, T=32")
plt.plot(maandag1, label = "after 70u, T=32")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("27 wt lut 30mM geen verdunning")
plt.xlabel("z level in \u00B5m")
plt.ylabel("Intensity per pixel - max value")
plt.show()

#%%


def manipulate2(the_list):
    new_list = []
       
    for i in range(np.argmax(the_list)-5, len(the_list)):
        try:
            avarage = begin1[i]
            new_list.append(the_list[i] - avarage)
        except:
            print("out of bound")
            
    return new_list
    
    
begin2 = manipulate2(begin1)
gel12 = manipulate2(gel11)
afgekoeld12 = manipulate2(afgekoeld11)
gel22 = manipulate2(gel21)
afterlongmeasure2 = manipulate2(afterlongmeasure1)
gel2_332 = manipulate2(gel2_331)
maandag2 = manipulate2(maandag1)    

plt.figure()
plt.plot(begin2, label = "begin, T=31")
plt.plot(gel12, label = "first time gel, T=33")
plt.plot(afgekoeld12, label = "afgekoeld (geen gel), T=31")
plt.plot(gel2_332, label = "tweede gel, T=33")
plt.plot(gel22, label = "Dezelfde gel (voor lange meting), T=32")
plt.plot(afterlongmeasure2, label = "na lange meting, T=32")
plt.plot(maandag2, label = "after 70u, T=32")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("27 wt lut 30mM geen verdunning")
plt.xlabel("z level in \u00B5m")
plt.ylabel("Intensity per pixel - max value and normalized; - begin(z)")
plt.show()

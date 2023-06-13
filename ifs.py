# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on May 12, 2023

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib as mpl
import numpy as np
#import time

# Creates a list of all sequences of length n of numbers between 1 and m
def codes(m, n):
    l = 0
    codes = []
    while l < m**n:
        k = l
        j = n - 1
        expan = []
        while j >= 0:
            expan.append(k // (m**j))
            if k // (m**j) != 0:
                k = k % (m**j)
            j -= 1
        l += 1
        codes.append(expan)
    return np.array(codes)


# TODO: fix aspect ratio
# TODO: dummy-proof?
# TODO: import from ifs.py
def plot(ifs, clicks, n = 0, grid = None, xlim = [0,1], ylim = [0,1], facecolor = 'k', edgecolor = 'k'):
    
    
    if grid == None:
        multiplot = False
        nrows = 1
        ncols = 1
    else:   
        multiplot = True
        nrows = grid[0]
        ncols = grid[1]
    
    fig, axs = plt.subplots(nrows = nrows, ncols = ncols)
    
    if nrows == 1 & ncols == 1:
        axs = np.array([axs])
    else:
        axs = axs.ravel()
    
    for ax in axs:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    
    m = len(ifs)
    
    #start = time.perf_counter()

    if multiplot == True:      
        
        for j, ax in enumerate(axs):  
            
            for code in codes(m, j):
                
                t = mpl.transforms.IdentityTransform()
                
                for i in code:
                    t += ifs[i]
                    
                ax.add_patch(mpl.patches.Polygon(t.transform(clicks), facecolor = facecolor, edgecolor = edgecolor))
            
            #end = time.perf_counter()
            #print('Iteration ' + str(j) + ' took ' + str(end - start) + ' seconds.') 
    else:      
        
        ax = axs[0]
        
        t = mpl.transforms.IdentityTransform()
        
        for code in codes(m, n):
            
            t = mpl.transforms.IdentityTransform()
            
            for i in code:
                    t += ifs[i]
        
            ax.add_patch(mpl.patches.Polygon(t.transform(clicks), facecolor = color))
        
        #end = time.perf_counter()
        #print('Iteration ' + str(n) + ' took ' + str(end - start) + ' seconds.')
        
    #plt.show()    
    
    #end = time.perf_counter()
    #print('The whole cell took ' + str(end - start) + ' seconds.')
    
    return fig





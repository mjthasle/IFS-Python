# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on Nov 27, 2024

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

# Create an IFS attractor class
class attractor:
    def __init__(self, ifs = None, clicks = None, xlim = [0,1], ylim = [0,1]):
        if ifs == None:
            self.ifs = []
        else:
            self.ifs = ifs
        self.clicks = clicks
        self.xlim = xlim 
        self.ylim = ylim 

    def plot(self, n = 0, grid = None, facecolor = 'k', edgecolor = 'k', showaxis = True):
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
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)
            ax.set_aspect("equal")

        if showaxis == False:
            for ax in axs:
                ax.set_axis_off()
        
        m = len(self.ifs)
        
        #start = time.perf_counter()

        if multiplot == True:      
            
            for j, ax in enumerate(axs):  
                
                for code in codes(m, j):
                    
                    t = mpl.transforms.IdentityTransform()
                    
                    for i in code:
                        t += self.ifs[i]
                        
                    ax.add_patch(mpl.patches.Polygon(t.transform(self.clicks), facecolor = facecolor, edgecolor = edgecolor))
                
                #end = time.perf_counter()
                #print('Iteration ' + str(j) + ' took ' + str(end - start) + ' seconds.') 
        else:      
            
            ax = axs[0]
            t = mpl.transforms.IdentityTransform()
            
            for code in codes(m, n):
                
                t = mpl.transforms.IdentityTransform()
                
                for i in code:
                        t += self.ifs[i]
            
                ax.add_patch(mpl.patches.Polygon(t.transform(self.clicks), facecolor = facecolor, edgecolor=edgecolor))
            
            #end = time.perf_counter()
            #print('Iteration ' + str(n) + ' took ' + str(end - start) + ' seconds.')

        #end = time.perf_counter()
        #print('The whole cell took ' + str(end - start) + ' seconds.')

        return fig


# Function to create a Cantor ternary set
def cantor():
    K = attractor(clicks=np.array([[0, 0], [1, 0]]),
        xlim = [-0.5, 1.5], ylim = [-0.5, 0.5])
    K.ifs.append(mpl.transforms.Affine2D().scale(1/3))
    K.ifs.append(mpl.transforms.Affine2D().translate(2/3, 0) + mpl.transforms.Affine2D().scale(1/3))
    return K

# Function to create a Sierpinski gasket
def gasket():
    K = attractor(clicks=np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]]))
    K.ifs.append(mpl.transforms.Affine2D().scale(0.5))
    K.ifs.append(mpl.transforms.Affine2D().translate(1, 0) + mpl.transforms.Affine2D().scale(0.5))
    K.ifs.append(mpl.transforms.Affine2D().translate(0.5, np.sqrt(3)/2) + mpl.transforms.Affine2D().scale(0.5))
    return K

# Function to create a fudgeflake
def fudgeflake():
    K = attractor(clicks=np.array([[0.2, 0.2], [1, 1], [0.75, 0.9], [0.2, 0.2], [0.75, 0.9], [0.5, 1]]),
        xlim = [-1,1], ylim = [-1,1])
    K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/6) + mpl.transforms.Affine2D().scale(1/np.sqrt(3)) + mpl.transforms.Affine2D().translate(-1/3, 0))
    K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/6) + mpl.transforms.Affine2D().scale(1/np.sqrt(3)) + mpl.transforms.Affine2D().translate(0.5*(1/3), (np.sqrt(3)/2)*(1/3)))
    K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/6) + mpl.transforms.Affine2D().scale(1/np.sqrt(3)) + mpl.transforms.Affine2D().translate(0.5*(1/3), -(np.sqrt(3)/2)*(1/3)))
    return K

# Function to create a twindragon
def twindragon():
    K = attractor(clicks=np.array([[0.2, 0.2], [1, 1], [0.75, 0.9], [0.2, 0.2], [0.75, 0.9], [0.5, 1]]),
        xlim = [-1.5,1.5], ylim = [-1.5, 1.5])
    K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/4) + mpl.transforms.Affine2D().translate(-0.5, 0.5) + mpl.transforms.Affine2D().scale(1/np.sqrt(2)))
    K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/4) + mpl.transforms.Affine2D().translate(0.5, -0.5) + mpl.transforms.Affine2D().scale(1/np.sqrt(2)))
    return K


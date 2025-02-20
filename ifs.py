# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on Feb 19, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import streamlit as st
import matplotlib as mpl
import numpy as np
import time
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None

file_path = os.path.join(os.getcwd(), "config.json")
with open(file_path, 'r', encoding = 'utf8') as json_file:
    config = json.load(json_file)

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

# Function to fix array spacing for latex equations
def texeq(eq, arrayspace=0.5, units="ex"):
    return eq.replace("\\\\", f"\\\\[{arrayspace}{units}]")

# Create an IFS attractor class with a method for plotting
class attractor:

    instances = []

    def __init__(self, namestring, ifs = None, funstrings = None, max_iterations = 10,
        clicks = None, xlim = [0,1], ylim = [0,1], grid = (1,1)):

        self.instances.append(namestring)

        if ifs == None:
            self.ifs = []
        else:
            self.ifs = ifs

        if funstrings == None:
            self.funstrings = []
        else:
            self.funstrings = funstrings

        self.clicks = clicks
        self.grid = grid
        self.xlim = xlim
        self.ylim = ylim
        self.max_iterations = max_iterations
        self.namestring = namestring

        if(self.namestring in list(config.keys())):
            self.grid = config[self.namestring]['grid']
            self.clicks = config[self.namestring]['clicks']
            self.xlim = config[self.namestring]['xlim']
            self.ylim = config[self.namestring]['ylim']
            self.max_iterations = config[self.namestring]['max_iterations']

    def add_fun(self, fun):
        self.ifs.append(fun)

    def add_funstring(self, funstring, addspace = True):
        if addspace:
            eq = texeq(funstring)
        else: eq = funstring
        self.funstrings.append(eq)

    def format_ax(self, ax):
        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
        ax.set_aspect("equal")
        old_ticks = ax.get_yticks()
        new_ticks = old_ticks[1:]
        ax.set_yticks(new_ticks)

    def plot(self, n = 0, facecolor = 'k',
        showaxis = True, timeit = False):

        nrows = 1
        ncols = 1
        assert n <= self.max_iterations, f"Max {self.max_iterations} iterations reached"

        fig, ax = plt.subplots(nrows = 1, ncols = 1)
        self.format_ax(ax)

        if showaxis == False:
            ax.set_axis_off()

        m = len(self.ifs)
        start = time.perf_counter()
        t = mpl.transforms.IdentityTransform()

        for code in codes(m, n):

            t = mpl.transforms.IdentityTransform()

            for i in code:
                    t += self.ifs[i]

            ax.add_patch(mpl.patches.Polygon(t.transform(self.clicks),
                facecolor = facecolor))

        end = time.perf_counter()

        if timeit:
            print('Iteration ' + str(n) + ' took ' + str(end - start) +
                ' seconds.')

        end = time.perf_counter()

        if timeit:
            print('The whole process took ' + str(end - start) + ' seconds.')

        st.pyplot(fig)


     # Function to show multiplots in steamlit one-by-one
    def multiplot(self, facecolor = 'k',
        showaxis = True, timeit = False, saveit = False):

        start = time.perf_counter()

        nrows = self.grid[0]
        ncols = self.grid[1]
        assert nrows*ncols <= self.max_iterations, f"Max {self.max_iterations} iterations reached"

        fig, axs = plt.subplots(nrows = nrows, ncols = ncols)

        if nrows == 1 & ncols == 1:
            axs = np.array([axs])
        else:
            axs = axs.ravel()

        for ax in axs:
            self.format_ax(ax)

        if showaxis == False:
            for ax in axs:
                ax.set_axis_off()

        end = time.perf_counter()

        if timeit:
            st.write("Initial set up time: " + str(end - start) + " seconds")

        start = time.perf_counter()
        the_plot = st.pyplot(fig)
        end = time.perf_counter()

        if timeit:
            st.write("Initial plot axes took " + str(end - start) + " seconds")

        m = len(self.ifs)

        for j, ax in enumerate(axs):

            start = time.perf_counter()

            for code in codes(m, j):

                t = mpl.transforms.IdentityTransform()

                for i in code:
                    t += self.ifs[i]

                ax.add_patch(mpl.patches.Polygon(t.transform(self.clicks),
                    facecolor = facecolor))

            the_plot.pyplot(fig)

            end = time.perf_counter()

            if timeit:
                st.write('Iteration ' + str(j) + ' took ' + str(end - start) +
                    ' seconds.')

class IFSCatalogue:
    # Function to create a Cantor ternary set (TODO: fix this plot)
    def cantor():
        K = attractor(namestring = "Cantor Ternary Set")

        K.ifs.append(mpl.transforms.Affine2D().scale(1/3))
        K.funstrings.append(r'''f_1(x) = \frac{1}{3}x''')

        K.ifs.append(mpl.transforms.Affine2D().translate(2, 0) +
            mpl.transforms.Affine2D().scale(1/3))
        K.funstrings.append(r'''f_2(x) = \frac{1}{3}x + \begin{bmatrix}
            \frac{2}{3} \\ 0
            \end{bmatrix}''')

        return K

    # Function to create a Sierpinski gasket
    def gasket():
        K = attractor(namestring = "Sierpinski Gasket")

        K.ifs.append(mpl.transforms.Affine2D().scale(0.5))
        K.funstrings.append(r'''f_1(x) = \frac{1}{2}x''')

        K.ifs.append(mpl.transforms.Affine2D().translate(1, 0) +
            mpl.transforms.Affine2D().scale(0.5))
        K.funstrings.append(r'''f_2(x) = \frac{1}{2}x +
            \begin{bmatrix}
            \frac{1}{2} \\ 0
            \end{bmatrix}''')

        K.ifs.append(mpl.transforms.Affine2D().translate(0.5, np.sqrt(3)/2) +
            mpl.transforms.Affine2D().scale(0.5))
        K.funstrings.append(r'''f_3(x) = \frac{1}{2}x +
            \begin{bmatrix}
            \frac{1}{4} \\
            \frac{\sqrt{3}}{4}
            \end{bmatrix}''')

        return K

    def carpet():
        K = attractor(namestring = "Sierpinski Carpet")

        for i in range(9):
            if i != 4:
                K.ifs.append(mpl.transforms.Affine2D().translate(i // 3, i % 3) + mpl.transforms.Affine2D().scale(1/3))
        K.funstrings.append(r'''f_{i,j}(x) = \frac{1}{3}\left(x+\begin{bmatrix}
            i \\
            j
            \end{bmatrix}\right)\text{ for }(i,j)\in\{0,1,2\}^2-\{(1,1)\}''')

        return K
    
    # Function to create a fudgeflake
    def fudgeflake():
        K = attractor(namestring = "Fudgeflake")

        K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/6) +
            mpl.transforms.Affine2D().scale(1/np.sqrt(3)) +
            mpl.transforms.Affine2D().translate(-1/3, 0))
        K.funstrings.append(r'''f_1(x) =
            \begin{bmatrix}
            \frac{1}{2} & -\frac{\sqrt{3}}{6} \\
            \frac{\sqrt{3}}{6} & \frac{1}{2}
            \end{bmatrix}x''')

        K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/6) +
            mpl.transforms.Affine2D().scale(1/np.sqrt(3)) +
            mpl.transforms.Affine2D().translate(0.5*(1/3), (np.sqrt(3)/2)*(1/3)))
        K.funstrings.append(r'''f_2(x) =
            \begin{bmatrix}
            \frac{1}{2} & -\frac{\sqrt{3}}{6} \\
            \frac{\sqrt{3}}{6} & \frac{1}{2}
            \end{bmatrix}x +
            \begin{bmatrix}
            \frac{1}{2} \\
            \frac{\sqrt{3}}{6}
            \end{bmatrix}''')

        K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/6) +
            mpl.transforms.Affine2D().scale(1/np.sqrt(3)) +
            mpl.transforms.Affine2D().translate(0.5*(1/3), -(np.sqrt(3)/2)*(1/3)))
        K.funstrings.append(r'''f_3(x) =
            \begin{bmatrix}
            \frac{1}{2} & -\frac{\sqrt{3}}{6} \\
            \frac{\sqrt{3}}{6} & \frac{1}{2}
            \end{bmatrix}x +
            \begin{bmatrix}
            \frac{1}{2} \\
            -\frac{\sqrt{3}}{6}
            \end{bmatrix}''')

        return K

    # Function to create a twindragon
    def twindragon():
        K = attractor(namestring = "Twindragon")

        K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/4) +
            mpl.transforms.Affine2D().translate(-0.5, 0.5) +
            mpl.transforms.Affine2D().scale(1/np.sqrt(2)))
        K.funstrings.append(r'''f_1(x) =
            \begin{bmatrix}
            \frac{1}{2} & -\frac{1}{2} \\
            \frac{1}{2} & \frac{1}{2}
            \end{bmatrix}x''')

        K.ifs.append(mpl.transforms.Affine2D().rotate(np.pi/4) +
            mpl.transforms.Affine2D().translate(0.5, -0.5) +
            mpl.transforms.Affine2D().scale(1/np.sqrt(2)))
        K.funstrings.append(r'''f_2(x) =
            \begin{bmatrix}
            \frac{1}{2} & -\frac{1}{2} \\
            \frac{1}{2} & \frac{1}{2}
            \end{bmatrix}x +
            \begin{bmatrix}
            \frac{1}{2} \\
            \frac{-1}{2}
            \end{bmatrix}''')

        return K

def get_attractors():
    attractors = [getattr(IFSCatalogue, method)() for method in dir(IFSCatalogue) if callable(getattr(IFSCatalogue, method)) and not method.startswith("__")]
    return attractors

def get_selected_attractor(option_selected, attractors):
    matches = [a for a in attractors if a.namestring == option_selected]
    assert len(matches) == 1, "More than one attractor has this name!"
    a = matches[0]
    return a

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on Nov 30, 2024

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import streamlit as st
import matplotlib as mpl
import numpy as np
import time
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None

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

    def __init__(self, ifs = None, funstrings=None, namestring=None,
        clicks = None, xlim = [0,1], ylim = [0,1]):

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
        self.namestring = namestring
        self.xlim = xlim
        self.ylim = ylim

    def add_fun(self, fun):
        self.ifs.append(fun)

    def add_funstring(self, funstring, addspace = True):
        if addspace:
            eq = texeq(funstring)
        else: eq = funstring
        self.funstrings.append(eq)

    def plot(self, n = 0, facecolor = 'k', edgecolor = 'k',
        showaxis = True, timeit = False):

        nrows = 1
        ncols = 1
        assert n <= 15, "Max 15 iterations reached"

        fig, axs = plt.subplots(nrows = 1, ncols = 1)
        axs = np.array([axs])

        for ax in axs:
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)
            ax.set_aspect("equal")
            old_ticks = ax.get_yticks()
            new_ticks = old_ticks[1:]
            ax.set_yticks(new_ticks)

        if showaxis == False:
            for ax in axs:
                ax.set_axis_off()

        m = len(self.ifs)
        start = time.perf_counter()
        ax = axs[0]
        t = mpl.transforms.IdentityTransform()

        for code in codes(m, n):

            t = mpl.transforms.IdentityTransform()

            for i in code:
                    t += self.ifs[i]

            ax.add_patch(mpl.patches.Polygon(t.transform(self.clicks),
                facecolor = facecolor, edgecolor = edgecolor))

        end = time.perf_counter()

        if timeit:
            print('Iteration ' + str(n) + ' took ' + str(end - start) +
                ' seconds.')

        end = time.perf_counter()

        if timeit:
            print('The whole process took ' + str(end - start) + ' seconds.')

        return fig


     # Function to show multiplots in steamlit one-by-one
    def multiplot(self, grid = (1,1), facecolor = 'k', edgecolor = 'k',
        showaxis = True, timeit = False, saveit = False):

        start = time.perf_counter()

        nrows = grid[0]
        ncols = grid[1]
        assert nrows*ncols <= 15, "Max 15 iterations reached"

        fig, axs = plt.subplots(nrows = nrows, ncols = ncols)

        if nrows == 1 & ncols == 1:
            axs = np.array([axs])
        else:
            axs = axs.ravel()

        for ax in axs:
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)
            ax.set_aspect("equal")
            old_ticks = ax.get_yticks()
            new_ticks = old_ticks[1:]
            ax.set_yticks(new_ticks)

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
                    facecolor = facecolor, edgecolor = edgecolor))

            the_plot.pyplot(fig)

            end = time.perf_counter()

            if timeit:
                st.write('Iteration ' + str(j) + ' took ' + str(end - start) +
                    ' seconds.')

class IFSCatalogue:
    # Function to create a Cantor ternary set (TODO: fix this plot)
    def cantor():
        K = attractor(clicks=np.array([[0, -0.5], [1, -0.5], [1, 0.5], [0, 0.5]]),
            xlim = [-0.25, 1.25], ylim = [-0.5, 0.5])

        K.ifs.append(mpl.transforms.Affine2D().scale(1/3))
        K.funstrings.append(r'''f_1 = \frac{1}{3}x''')

        K.ifs.append(mpl.transforms.Affine2D().translate(2, 0) +
            mpl.transforms.Affine2D().scale(1/3))
        K.funstrings.append(r'''f_2 = \frac{1}{3}x + \frac{2}{3}''')

        K.namestring = "Cantor Ternary Set"
        return K

    # Function to create a Sierpinski gasket
    def gasket():
        K = attractor(clicks=np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]]))

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

        K.namestring = "Sierpinski Gasket"
        return K

    # Function to create a fudgeflake
    def fudgeflake():
        K = attractor(clicks=np.array([[0.2, 0.2], [1, 1], [0.75, 0.9], [0.2, 0.2],
            [0.75, 0.9], [0.5, 1]]),
            xlim = [-1,1], ylim = [-1,1])

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

        K.namestring = "Fudgeflake"
        return K

    # Function to create a twindragon
    def twindragon():
        K = attractor(clicks=np.array([[0.2, 0.2], [1, 1], [0.75, 0.9], [0.2, 0.2],
            [0.75, 0.9], [0.5, 1]]),
            xlim = [-1.5,1.5], ylim = [-1.5, 1.5])

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

        K.namestring = "Twindragon"
        return K

def get_attractors():
    attractors = [getattr(IFSCatalogue, method)() for method in dir(IFSCatalogue) if callable(getattr(IFSCatalogue, method)) and not method.startswith("__")]
    return attractors

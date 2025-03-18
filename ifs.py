# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on March 17, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.transforms import Affine2D, IdentityTransform
import streamlit as st
import matplotlib as mpl
import numpy as np
import time

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

# Functions to fix array spacing for latex equations
def texeq(eq, arrayspace = 0.5, units = "ex"):
    return eq.replace("\\\\", f"\\\\[{arrayspace}{units}]")

def fix_tex(oldstrings):
    return [texeq(s) for s in oldstrings]

# Create an IFS attractor class with a method for plotting
class attractor:

    instances = []

    def __init__(self, namestring, ifs = None):

        self.instances.append(namestring)

        self.namestring = namestring

        if ifs == None:
            self.ifs = []
        else:
            self.ifs = ifs

        built_in_ifs = config['built_in_ifs']
        built_in_ifs_keys = list(built_in_ifs.keys())

        assert self.namestring in built_in_ifs_keys, "Attractor missing"

        assert built_in_ifs_keys != config['required_fields'], "Incorrect \
            fields in attractor data"

        self.grid = built_in_ifs[self.namestring]['grid']
        self.xlim = built_in_ifs[self.namestring]['xlim']
        self.ylim = built_in_ifs[self.namestring]['ylim']
        self.max_iterations = built_in_ifs[self.namestring]['max_iterations']
        self.funstrings = fix_tex(built_in_ifs[self.namestring]['funstrings'])

    def add_fun(self, fun):
        self.ifs.append(fun)

    def format_ax(self, ax):
        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
        ax.set_aspect("equal")
        old_ticks = ax.get_yticks()
        new_ticks = old_ticks[1:]
        ax.set_yticks(new_ticks)

    def plot(self, n = 0, facecolor = 'k',
        showaxis = True, showgridlines = False, timeit = False,
        clicks = [[0,0], [0,1], [1,0]]):

        nrows = 1
        ncols = 1
        assert n <= self.max_iterations, f"Max {self.max_iterations} \
            iterations reached"

        fig, ax = plt.subplots(nrows = 1, ncols = 1)
        self.format_ax(ax)

        if showaxis == False:
            ax.set_axis_off()

        if showgridlines:
            ax.grid(alpha = 0.5)

        m = len(self.ifs)
        start = time.perf_counter()
        t = IdentityTransform()

        for code in codes(m, n):

            t = IdentityTransform()

            for i in code:
                    t += self.ifs[i]

            ax.add_patch(Polygon(t.transform(clicks),
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
        showaxis = True, showgridlines = False, timeit = False, saveit = False,
        clicks = [[0,0], [0,1], [1,0]]):

        start = time.perf_counter()

        nrows = self.grid[0]
        ncols = self.grid[1]
        assert nrows*ncols <= self.max_iterations, f"Max {self.max_iterations} \
            iterations reached"

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

        if showgridlines:
            for ax in axs:
                ax.grid(alpha = 0.5)

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

                ax.add_patch(mpl.patches.Polygon(t.transform(clicks),
                    facecolor = facecolor))

            the_plot.pyplot(fig)

            end = time.perf_counter()

            if timeit:
                st.write('Iteration ' + str(j) + ' took ' + str(end - start) +
                    ' seconds.')

class IFSCatalogue:
    # Function to create a Cantor ternary set
    def cantor():
        K = attractor(namestring = "Cantor Ternary Set")

        K.ifs.append(Affine2D().scale(1/3))

        K.ifs.append(Affine2D().translate(2, 0) + Affine2D().scale(1/3))

        return K

    # Function to create a Sierpinski gasket
    def gasket():
        K = attractor(namestring = "Sierpinski Gasket")

        K.ifs.append(Affine2D().scale(0.5))

        K.ifs.append(Affine2D().translate(1, 0) + Affine2D().scale(0.5))

        K.ifs.append(Affine2D().translate(0.5, np.sqrt(3)/2) +
            Affine2D().scale(0.5))

        return K

    def carpet():
        K = attractor(namestring = "Sierpinski Carpet")

        for i in range(9):
            if i != 4:
                K.ifs.append(Affine2D().translate(i // 3, i % 3)
                    + Affine2D().scale(1/3))

        return K

    # Function to create a fudgeflake
    def fudgeflake():
        K = attractor(namestring = "Fudgeflake")

        K.ifs.append(Affine2D().rotate(np.pi/6) +
            Affine2D().scale(1/np.sqrt(3)) +
            Affine2D().translate(-1/3, 0))

        K.ifs.append(Affine2D().rotate(np.pi/6) +
            Affine2D().scale(1/np.sqrt(3)) +
            Affine2D().translate(0.5*(1/3),(np.sqrt(3)/2)*(1/3)))

        K.ifs.append(Affine2D().rotate(np.pi/6) +
            Affine2D().scale(1/np.sqrt(3)) +
            Affine2D().translate(0.5*(1/3),-(np.sqrt(3)/2)*(1/3)))

        return K

    # Function to create a twindragon
    def twindragon():
        K = attractor(namestring = "Twindragon")

        K.ifs.append(Affine2D().rotate(np.pi/4) +
            Affine2D().translate(-0.5, 0.5) +
            Affine2D().scale(1/np.sqrt(2)))

        K.ifs.append(Affine2D().rotate(np.pi/4) +
            Affine2D().translate(0.5, -0.5) +
            Affine2D().scale(1/np.sqrt(2)))

        return K

def get_attractors():
    attractors = [getattr(IFSCatalogue, method)() for method \
        in dir(IFSCatalogue) if callable(getattr(IFSCatalogue, method)) \
        and not method.startswith("__")]
    return attractors

def get_selected_attractor(option_selected, attractors):
    matches = [a for a in attractors if a.namestring == option_selected]
    assert len(matches) == 1, "More than one attractor has this name!"
    a = matches[0]

    return a

def get_initial_set(option_selected):
    attractors = get_attractors()
    a = get_selected_attractor(option_selected, attractors)
    initial_set = config["built_in_ifs"][a.namestring]["initial_set"]
    return initial_set

def get_default_index(option_selected):
    initial_set = get_initial_set(option_selected)
    options = list(config['initial_sets'])
    default_index = options.index(initial_set)
    return default_index

def reset_n():
    st.session_state.n = 0

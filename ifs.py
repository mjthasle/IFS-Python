# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on May 27, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import os
from importlib import import_module
import json
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib as mpl
import numpy as np
import time
from matplotlib.transforms import IdentityTransform
from matplotlib.patches import Polygon

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

    def __init__(self, namestring):

        self.instances.append(namestring)

        self.namestring = namestring

        built_in_ifs = config['built_in_ifs']
        built_in_ifs_keys = list(built_in_ifs.keys())
        functions_dir = config['functions_dir']

        assert self.namestring in built_in_ifs_keys, "Attractor missing"

        assert built_in_ifs_keys != config['required_fields'], "Incorrect \
            fields in attractor data"

        self.grid = built_in_ifs[self.namestring]['grid']
        self.xlim = built_in_ifs[self.namestring]['xlim']
        self.ylim = built_in_ifs[self.namestring]['ylim']
        self.max_iterations = built_in_ifs[self.namestring]['max_iterations']
        self.funstrings = fix_tex(built_in_ifs[self.namestring]['funstrings'])
        self.ifs_script = functions_dir + "." + built_in_ifs[self.namestring]['ifs_script']

        # Run script to retrieve affine transforms
        ifs_script = import_module(self.ifs_script)
        get_ifs = getattr(ifs_script, "get_ifs")
        self.ifs = get_ifs()


    def add_fun(self, fun):
        self.ifs.append(fun)

    def format_ax(self, ax, set_lim = False):
        if set_lim:
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)
        ax.set_aspect("equal")
        old_ticks = ax.get_yticks()
        new_ticks = old_ticks[1:]
        ax.set_yticks(new_ticks)

    def plot(self, n = 0, facecolor = 'k',
        showaxis = True, showgridlines = False, set_lim = False, timeit = False,
        clicks = [[0,0], [0,1], [1,0]]):

        nrows = 1
        ncols = 1
        assert n <= self.max_iterations, f"Max {self.max_iterations} \
            iterations reached"

        fig, ax = plt.subplots(nrows = 1, ncols = 1)  # This can be simplified
        self.format_ax(ax, set_lim=set_lim)

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

        if not set_lim:
            ax.autoscale()

        st.pyplot(fig)


     # Function to show multiplots in steamlit one-by-one
    def multiplot(self, facecolor = 'k',
        showaxis = True, showgridlines = False, set_lim = False, timeit = False,
        saveit = False, clicks = [[0,0], [0,1], [1,0]]):

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
            self.format_ax(ax, set_lim)

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

                t = IdentityTransform()

                for i in code:
                    t += self.ifs[i]

                ax.add_patch(Polygon(t.transform(clicks),
                    facecolor = facecolor))

            if not set_lim:
                ax.autoscale()

            the_plot.pyplot(fig)

            end = time.perf_counter()

            if timeit:
                st.write('Iteration ' + str(j) + ' took ' + str(end - start) +
                    ' seconds.')

def get_attractors():
    built_in_ifs = config['built_in_ifs']
    built_in_ifs_keys = list(built_in_ifs.keys())
    attractors = []
    for ifs_key in built_in_ifs_keys:
        K = attractor(namestring = ifs_key)
        attractors.append(K)
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

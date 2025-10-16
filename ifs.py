# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

Last Updated on Oct 15, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import os
from importlib import import_module
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st
import matplotlib as mpl
import numpy as np
import time
from matplotlib.transforms import IdentityTransform
from matplotlib.patches import Polygon
import ast
import re

file_path = os.path.join(os.getcwd(), "config.json")
with open(file_path, 'r', encoding = 'utf8') as json_file:
    config = json.load(json_file)

canvas_dimension = config["canvas_dimension"]
colour_default = config["colour_default"]

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

def get_coordinates(raw_coords):
    new_list = []
    coord_dict = list(raw_coords)
    for pair in coord_dict:
        if len(pair) > 1:
            new_list.append([(1 / canvas_dimension) * float(pair[1]), 
                (-1 / canvas_dimension) * float(pair[2]) + 1])
    return new_list

# Functions to fix array spacing for latex equations
def texeq(eq, arrayspace = 0.5, units = "ex"):
    return eq.replace("\\\\", f"\\\\[{arrayspace}{units}]")

def fix_tex(oldstrings):
    return [texeq(s) for s in oldstrings]

# Create an IFS attractor class with a method for plotting
class attractor:

    instances = []

    def __init__(self, namestring=None, IFS=None, grid=None, xlim=None, 
        ylim=None):

        # Built-in IFS 
        if namestring is not None and IFS is None:
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
            self.funstrings = fix_tex(
                built_in_ifs[self.namestring]['funstrings'])
            self.ifs_script = functions_dir + "." + \
                built_in_ifs[self.namestring]['ifs_script']

            # Run script to retrieve affine transforms
            ifs_script = import_module(self.ifs_script)
            get_ifs = getattr(ifs_script, "get_ifs")
            self.ifs = get_ifs()

        # Build-your-own IFS
        else:
            self.ifs = IFS 
            self.grid = grid
            self.xlim = xlim
            self.ylim = ylim
            self.max_iterations = config['max_iterations_default']

    def format_ax(self, ax, set_lim = False):
        if set_lim:
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)
        ax.set_aspect("equal")
        old_ticks = ax.get_yticks()
        new_ticks = old_ticks[1:]
        ax.set_yticks(new_ticks)

    def format_auto_ax(self, ax):
        ax.autoscale()

        # make the xlims and ylims the same
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        lim_min = min(xlim[0], ylim[0])
        lim_max = max(xlim[1], ylim[1])
        lim = [lim_min, lim_max]
        ax.set_xlim(lim)
        ax.set_ylim(lim)

        # Change x-axis and y-axis tick spacing
        # Ticks at multiples of base
        nticks = 4
        ax.xaxis.set_major_locator(plt.MaxNLocator(nticks))
        ax.yaxis.set_major_locator(plt.MaxNLocator(nticks))

    # set_lim = False automatically chooses the xlim and ylim parameters 
    def plot(self, n = 0, facecolor = colour_default,
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
        t = mpl.transforms.IdentityTransform()

        for code in codes(m, n):

            t = mpl.transforms.IdentityTransform()

            for i in code:
                t += self.ifs[i]

            ax.add_patch(mpl.patches.Polygon(t.transform(clicks),
                facecolor = facecolor))

        end = time.perf_counter()

        if timeit:
            print('Iteration ' + str(n) + ' took ' + str(end - start) +
                ' seconds.')

        end = time.perf_counter()

        if timeit:
            print('The whole process took ' + str(end - start) + ' seconds.')

        if not set_lim:
            self.format_auto_ax(ax)

        return fig


     # Function to show multiplots in steamlit one-by-one

    def multiplot(self, facecolor=colour_default,
              showaxis=True, showgridlines=False, set_lim=False, timeit=False, 
              saveit=False, clicks=[[0,0], [0,1], [1,0]]):

        start = time.perf_counter()
        nrows = self.grid[0]
        ncols = self.grid[1]

        assert nrows * ncols <= self.max_iterations, \
            f"Max {self.max_iterations} iterations reached"

        fig, axs = plt.subplots(nrows=nrows, ncols=ncols)

        # Ensure axs is always a flat array
        if nrows == 1 and ncols == 1:
            axs = np.array([axs])
        else:
            axs = axs.ravel()

        for ax in axs:
            self.format_ax(ax, set_lim)

        if not showaxis:
            for ax in axs:
                ax.set_axis_off()

        if showgridlines:
            for ax in axs:
                ax.grid(alpha=0.5)

        end = time.perf_counter()

        if timeit:
            st.write("Initial set up time: " + str(end - start) + " seconds")

        start = time.perf_counter()
        the_plot = st.pyplot(fig)
        end = time.perf_counter()

        m = len(self.ifs)

        for j, ax in enumerate(axs):
            start = time.perf_counter()

            for code in codes(m, j):
                t = IdentityTransform()
                for i in code:
                    t += self.ifs[i]
                ax.add_patch(Polygon(t.transform(clicks), facecolor=facecolor))

            # Autoscale axes if manual limits are not set
            if not set_lim:
                self.format_auto_ax(ax)

            # Plot the iteration
            the_plot.pyplot(fig)

            end = time.perf_counter()
            if timeit:
                st.write('Iteration ' + str(j) + ' took ' + str(end - start) +
                 ' seconds.')

        # Return the final figure to be saved in session state
        return fig

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

def get_default_index(option_selected=None):

    initial_set = config['initial_set_default']

    if option_selected is not None:
        initial_set = get_initial_set(option_selected)

    options = list(config['initial_sets'])
    default_index = options.index(initial_set)
    return default_index

def reset_n():
    st.session_state.n = 0


import numpy as np
from fractions import Fraction
from typing import List

def str_to_numpy_array(input_str):
    """
    Parse a string of the form "[[a,b,...],[c,d,...],...]" into an n×m numpy 
    array.
    Supports integers, floats, and fractions like "1/2".
    Internally returns dtype=float.
    """
    # Strip outer spaces
    s = input_str.strip()

    # Remove outermost brackets if present
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]

    rows = s.split("],")

    matrix: List[List[float]] = []
    for row in rows:
        row = row.replace("[", "").replace("]", "").strip()
        if not row:
            continue

        entries = row.split(",")
        parsed_row: List[float] = []
        for entry in entries:
            entry = entry.strip()
            if entry == "":
                raise ValueError("Empty matrix entry found")
            try:
                val = float(Fraction(entry))
            except (ValueError, ZeroDivisionError) as e:
                raise ValueError(f"Invalid number format: {entry}") from e
            parsed_row.append(val)

        matrix.append(parsed_row)

    if not matrix:
        return np.array(matrix, dtype=float)

    row_lengths = [len(r) for r in matrix]
    if any(length != row_lengths[0] for length in row_lengths):
        raise ValueError("Rows have inconsistent lengths")

    return np.array(matrix, dtype=float)


def array_to_latex(matrix):
    """
    Convert a 2D numpy array into a LaTeX bmatrix string.
    Rules:
      - If a value is an integer, print it as an integer.
      - Otherwise print it rounded to max 3 decimal places, 
        trimming unnecessary trailing zeros.
    """
    if matrix.ndim != 2:
        raise ValueError("Input must be a 2D array")

    rows_str = []
    for row in matrix:
        entries = []
        for val in row:
            f = float(val)

            if np.isnan(f):
                entries.append(r"\text{NaN}")
            elif np.isposinf(f):
                entries.append(r"\infty")
            elif np.isneginf(f):
                entries.append(r"-\infty")
            elif f.is_integer():
                entries.append(str(int(round(f))))
            else:
                # round to 3 decimal places and strip trailing zeros
                s = f"{f:.3f}".rstrip("0").rstrip(".")
                entries.append(s)
        rows_str.append(" & ".join(entries))

    body = r" \\ ".join(rows_str)
    return f"\\begin{{bmatrix}} {body} \\end{{bmatrix}}"


# Regex validator for matrix bracket structure
# Accept forms like: [[a,b],[c,d]] with optional whitespace
def matrix_bracket_ok(s):
    return bool(re.match(r'^\s*\[\s*\[[^\]]*\]\s*,\s*\[[^\]]*\]\s*\]\s*$', s))

# Regex validator for matrix bracket structure
# Accept forms like: [[a],[b]] with optional whitespace
def shift_bracket_ok(s):
    return bool(re.match(r'^\s*\[\s*\[[^\]]*\]\s*,\s*\[[^\]]*\]\s*\]\s*$', s))

def affine_to_strings(transform):
    a, b, c, d, e, f = transform.to_values()
    matrix_str = f"[[{a},{b}],[{c},{d}]]"
    shift_str = f"[[{e}],[{f}]]"
    return [matrix_str, shift_str]
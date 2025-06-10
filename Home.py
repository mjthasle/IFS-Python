# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:49:59 2023

Last Updated on May 27, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

from ifs import *

st.set_page_config(layout="wide")

st.title("IFS Python")

st.markdown("*Created by Mitch Haslehurst, PhD and Emily Korfanty*")

st.write("This app uses Python to generate fractal images from 2D affine iterated function systems.")

st.write("A 2D affine iterated function system (IFS) is any collection of functions of the form")

st.latex("$f(x) = Ax + b")

st.write("where...")

st.write("This app let's you explore attractors of 2D affine IFS by")

st.write("List pages and what they are")

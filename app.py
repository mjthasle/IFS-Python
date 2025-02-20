# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:49:59 2023

Last Updated on Feb 19, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import os
import json
import streamlit as st
from ifs import *

file_path = os.path.join(os.getcwd(), "config.json")
with open(file_path, 'r', encoding = 'utf8') as json_file:
    config = json.load(json_file)

st.set_page_config(layout="wide")

st.title("Let's draw IFS attractors!")

st.write("Use the drop-down menu to select a built-in iterated function system (IFS).  The plots show the result of iterating the IFS starting from a polygon.  No matter what polygon you start with, the results approximate the IFS attractor as the number of iterations increases!")

st.write("Turn off the toggle below to view a single iteration.")

multiplot = st.toggle("Multiplot", value=True)

if multiplot:
	plt.rcParams.update({'font.size': config['multiplot_font']})
	plt.rcParams['figure.figsize'] = config['multiplot_size']
else:
	plt.rcParams.update({'font.size': config['singleplot_font']})

col1, col2 = st.columns(2, gap = "large")

# built-in IFS options
attractors = get_attractors()
box_options = [a.namestring for a in attractors]

def reset_n():
	st.session_state.n = 0

# built-in IFS settings in the left column
with col1:
	option_selected = st.selectbox("Select an IFS attractor to plot",
		box_options, on_change = reset_n)

	a = get_selected_attractor(option_selected, attractors)
	max_iterations = a.max_iterations

	if not multiplot:
		n = st.number_input("Number of iterations: ", min_value = 0,
			max_value = max_iterations, step = 1, key = "n")

	for a in attractors:
		if a.namestring == option_selected:
			funstrings = a.funstrings
	for funstring in funstrings:
		st.latex(funstring)

# plot the attractor in the right column
with col2:
	a = get_selected_attractor(option_selected, attractors)
	if multiplot:
		if option_selected == "Cantor Ternary Set":
			a.multiplot()
		elif option_selected == "Sierpinski Gasket":
			a.multiplot()
		elif option_selected == "Fudgeflake":
			a.multiplot(facecolor = 'b')
		elif option_selected == "Twindragon":
			a.multiplot(facecolor = 'w')
	else:
		if option_selected == "Cantor Ternary Set":
			st.pyplot(a.plot(n = n))
		elif option_selected == "Sierpinski Gasket":
			st.pyplot(a.plot(n = n))
		elif option_selected == "Fudgeflake":
			st.pyplot(a.plot(n = n, facecolor = 'b'))
		elif option_selected == "Twindragon":
			st.pyplot(a.plot(n = n, facecolor = 'w'))

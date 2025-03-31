# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:49:59 2023

Last Updated on March 17, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

from ifs import *

st.set_page_config(layout="wide")

st.title("IFS Python")

st.markdown("*Created by Mitch Haslehurst, PhD and Emily Korfanty*")

st.write("This app uses Python to generate fractal images from two-dimensional \
	affine iterated function systems.")

st.write("Use the drop-down menu to select a built-in iterated function system \
	(IFS).  The plots show the result of iterating the IFS starting from a \
	polygon. No matter what polygon you start with, the results approximate \
	the IFS attractor as the number of iterations increases!")

st.write("Use the Multiplot toggle to change between views of individual \
	iterations and multiple iterations on the same canvas.")

multiplot = st.toggle("Multiplot", value = True)
gridlines = st.toggle("Show grid", value = True)
self_sim_color = st.toggle("Colour self-similarity", value = False)

if multiplot:
	plt.rcParams.update({'font.size': config['multiplot_font']})
	plt.rcParams['figure.figsize'] = config['multiplot_size']
else:
	plt.rcParams.update({'font.size': config['singleplot_font']})

col1, col2 = st.columns(2, gap = "large")

# built-in IFS options
attractors = get_attractors()
box_options = [a.namestring for a in attractors]
colour_options = config['colour_options']
initial_set_options = config['initial_sets']

# built-in IFS settings in the left column
with col1:
	option_selected = st.selectbox("Select an attractor to plot",
		box_options, on_change = reset_n)

	colour_selected = st.selectbox("Select a colour for the attractor",
								colour_options)
	
	if self_sim_color:
		colour_selected_1 = st.selectbox("Select a second colour to display self-similarity",
								   colour_options)
	else:
		colour_selected_1 = colour_selected

	initial_set_selected = st.selectbox("Select an initial set",
								initial_set_options.keys(),
								on_change = reset_n,
								index = get_default_index(option_selected))

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
	clicks = initial_set_options[initial_set_selected]
	if multiplot:
		a.multiplot(showgridlines = gridlines, facecolor = colour_selected, facecolor1 = colour_selected_1,
			clicks = clicks)
	else:
		a.plot(n = n, showgridlines = gridlines, facecolor = colour_selected, facecolor1 = colour_selected_1,
			clicks = clicks)

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:49:59 2023

Last Updated on March 3, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

from ifs import *

st.set_page_config(layout="wide")

st.title("Let's draw IFS attractors!")

st.write("Use the drop-down menu to select a built-in iterated function system (IFS).  The plots show the result of iterating the IFS starting from a polygon.  No matter what polygon you start with, the results approximate the IFS attractor as the number of iterations increases!")

st.write("Turn off the toggle below to view a single iteration.")

multiplot = st.toggle("Multiplot", value = False)

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

def reset_n():
	st.session_state.n = 0

# built-in IFS settings in the left column
with col1:
	option_selected = st.selectbox("Select an attractor to plot",
		box_options, on_change = reset_n)
	colour_selected = st.selectbox("Select a colour for the attractor",
								colour_options)

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
		a.multiplot(facecolor = colour_selected)
	else:
		a.plot(n = n, facecolor = colour_selected)

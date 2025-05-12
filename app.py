# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:49:59 2023

Last Updated on May 12, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

from ifs import *
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from threading import RLock

check = True

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

if multiplot:
	plt.rcParams.update({'font.size': config['multiplot_font']})
	plt.rcParams['figure.figsize'] = config['multiplot_size']
else:
	plt.rcParams.update({'font.size': config['singleplot_font']})

drawing_mode = st.sidebar.selectbox(
    "Drawing tool:",
    ("transform", "polygon", "point"),
)
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
realtime_update = st.sidebar.checkbox("Update in realtime", True)

# Create a canvas component
canvas_result = st_canvas(
    fill_color = stroke_color,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image = None,
    update_streamlit=realtime_update,
    height = 600,
	width = 600,
    drawing_mode=drawing_mode,
    point_display_radius = 0,
    display_toolbar = True,
    key="full_app",
)

# Do something interesting with the image data and paths
#if canvas_result.image_data is not None:
 #   st.image(canvas_result.image_data)
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
  #  objects_str = objects
#for col in objects_str.select_dtypes(include=["object"]).columns:
#	objects_str[col] = objects_str[col].astype("str")
#st.dataframe(objects_str)

coordinates = objects["path"][0]
colour = objects["fill"][0]
st.write(f"The coordinates are {coordinates} and the colour is {colour}")

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
	if check:
		colour_selected = colour

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
	if check:
		clicks = get_coordinates(coordinates)
	else:
		clicks = initial_set_options[initial_set_selected]
	_lock = RLock()
	with _lock:
		if multiplot:
			a.multiplot(showgridlines = gridlines, facecolor = colour_selected,
				clicks = clicks)
		else:
			a.plot(n = n, showgridlines = gridlines, facecolor = colour_selected,
				clicks = clicks)

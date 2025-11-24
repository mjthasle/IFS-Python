# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:49:59 2023

Last Updated on Oct 15, 2025

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

import io
from PIL import Image
from ifs import *
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from threading import RLock

st.set_page_config(layout = "wide")

st.header("Classical IFS")


st.write("Use the drop-down menu to select a built-in iterated function system \
	(IFS).  The plots show the result of iterating the IFS starting from a \
	polygon. No matter what polygon you start with, the results approximate \
	the IFS attractor as the number of iterations increases!")

st.write("Use the Multiplot toggle to change between views of individual \
	iterations and multiple iterations on the same canvas.")

# Classical IFS options
attractors = get_attractors()
box_options = [a.namestring for a in attractors]
initial_set_options = config['initial_sets']

option_selected = st.selectbox("Select an attractor to plot",
		box_options, on_change = reset_n)

a = get_selected_attractor(option_selected, attractors)
max_iterations = a.max_iterations

with st.expander("Show functions"):
	for a in attractors:
		if a.namestring == option_selected:
			funstrings = a.funstrings
	for funstring in funstrings:
		st.latex(funstring)

drawing_canvas = st.toggle("Draw initial polygon", value = False)

drawing_mode = "polygon"

stroke_width = 3

multiplot = st.toggle("Multiplot", value = True)
gridlines = st.toggle("Show grid", value = True)

if multiplot:
	plt.rcParams.update({'font.size': config['multiplot_font']})
	plt.rcParams['figure.figsize'] = config['multiplot_size']
else:
	plt.rcParams.update({'font.size': config['singleplot_font']})

# built-in IFS options
attractors = get_attractors()
box_options = [a.namestring for a in attractors]

col1, col2 = st.columns(2, gap = "medium")


# IFS settings in the left column

with col1:

	stroke_color = st.color_picker("Select a colour for the attractor: ", 
		colour_default)

	if not drawing_canvas:
		initial_set_selected = st.selectbox("Select an initial set",
									initial_set_options.keys(),
									on_change = reset_n,
									index = get_default_index(option_selected))
	if not multiplot:
		n = st.number_input("Number of iterations: ", min_value = 0,
			max_value = max_iterations, step = 1, key = "n")
	if drawing_canvas:
		fig, ax = plt.subplots()
		ax.grid(alpha = 0.75)
		fig.tight_layout(pad = 0.1)

		# 2. Create an in-memory buffer
		img_buf = io.BytesIO()

		# 3. Save the figure to the buffer
		fig.savefig(img_buf, format = 'png')

		# 4. Seek to the beginning of the buffer
		img_buf.seek(0)

		# 5. Open the image from the buffer with PIL
		pil_img = Image.open(img_buf)
		canvas_result = st_canvas(
			fill_color = stroke_color,
			stroke_width = stroke_width,
			stroke_color = stroke_color,
			background_color = "#eee",
			background_image = pil_img,
			update_streamlit = True,
			height = canvas_dimension,
			width = canvas_dimension,
			drawing_mode = drawing_mode,
			point_display_radius = 0,
			display_toolbar = True,
			key = "full_app",
		)
		img_buf.close()
	else:
		canvas_result = None
		colour_selected = stroke_color

	if canvas_result is not None:
		if canvas_result.json_data is not None:
			objects = pd.json_normalize(canvas_result.json_data["objects"])
			if len(objects) > 0:
				coordinates = objects["path"][0]

		colour_selected = stroke_color

# plot the attractor in the right column
with col2:
	a = get_selected_attractor(option_selected, attractors)
	set_lim = not option_selected == "Random IFS"

	if drawing_canvas:
		try:
			clicks = get_coordinates(coordinates)
		except (TypeError, KeyError, NameError):
			clicks = [[0, 0]]
	else:
		clicks = initial_set_options[initial_set_selected]
	_lock = RLock()
	with _lock:
		if multiplot:
			fig = a.multiplot(showgridlines = gridlines, 
				facecolor = colour_selected, set_lim = set_lim,clicks = clicks)
		else:
			fig = a.plot(n = n, showgridlines = gridlines, 
				facecolor = colour_selected, set_lim = set_lim, clicks = clicks)
			st.pyplot(fig)

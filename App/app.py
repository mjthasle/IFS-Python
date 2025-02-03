import os
import json
import streamlit as st
from ifs import *

file_path = os.path.join(os.getcwd(), "config.json")
with open(file_path, 'r', encoding = 'utf8') as json_file:
    config = json.load(json_file)

max_iterations = config["max_iterations"]

st.set_page_config(layout="wide")

st.title("Let's draw IFS attractors!")
st.header("Built-in IFS")

multiplot = st.toggle("Multiplot", value=True)

if multiplot:
	plt.rcParams.update({'font.size': 4})
	plt.rcParams['figure.figsize'] = (8,8)
else:
	plt.rcParams.update({'font.size': 10})
	#plt.rcParams['figure.figsize'] = (16, 16)

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
	matches = [a for a in attractors if a.namestring == option_selected]
	assert(len(matches) == 1, "More than one attractor has this name!")
	a = matches[0]
	if multiplot:
		if option_selected == "Cantor Ternary Set":
			a.multiplot(grid = (3,2))
		elif option_selected == "Sierpinski Gasket":
			a.multiplot(grid = (3,2))
		elif option_selected == "Fudgeflake":
			a.multiplot(grid = (3,3), facecolor = 'b')
		elif option_selected == "Twindragon":
			a.multiplot(grid = (4,3), facecolor = 'w')
	else:
		if option_selected == "Cantor Ternary Set":
			st.pyplot(a.plot(n = n))
		elif option_selected == "Sierpinski Gasket":
			st.pyplot(a.plot(n = n))
		elif option_selected == "Fudgeflake":
			st.pyplot(a.plot(n = n, facecolor = 'b'))
		elif option_selected == "Twindragon":
			st.pyplot(a.plot(n = n, facecolor = 'w'))

st.header("Random IFS")

st.write("Under construction.")

st.header("Make your own IFS")

st.write("Under construction.")

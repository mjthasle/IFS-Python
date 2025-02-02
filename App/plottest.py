import streamlit as st
from ifs import *
st.set_page_config(layout="wide")

# built-in IFS attractors
attractors = get_attractors()
box_options = ["Sierpinski Gasket", "Fudgeflake", "Twindragon"]
box_options = [a.namestring for a in attractors]

option_selected = st.selectbox("Select an IFS attractor to plot",
		box_options)

multiplot = st.toggle("Multiplot")

if(multiplot):
	if(option_selected == "Sierpinski Gasket"):
		start = time.perf_counter()
		gasket().multiplot(grid = (3,2), timeit = True)
		end = time.perf_counter()
		st.write('Total multiplot time: ' + str(end - start) + ' seconds.')
	else:
		st.write("Not testing")
else:
	st.write("No multiplot!")

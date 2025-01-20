import streamlit as st
from ifs import *

st.set_page_config(layout="wide")

st.title("Let's draw IFS attractors!")
st.header("Built-in IFS")

multiplot = st.toggle("Multiplot")

if multiplot:
	plt.rcParams['figure.figsize'] = (80, 80)
	plt.rcParams.update({'font.size': 35})
else:
	plt.rcParams['figure.figsize'] = (16, 16)
	plt.rcParams.update({'font.size': 12})

col1, col2 = st.columns(2, gap = "large")

# built-in IFS options
attractors = get_attractors()
box_options = ["Sierpinski Gasket", "Fudgeflake", "Twindragon"]
box_options = [a.namestring for a in attractors]

def reset_n():
	st.session_state.n = 0

# built-in IFS settings in the left column
with col1:
	option_selected = st.selectbox("Select an IFS attractor to plot",
		box_options, on_change = reset_n)
	n = st.number_input("Number of iterations: ", min_value = 0, max_value = 10,
		step = 1, key = "n")
	for a in attractors:
		if a.namestring == option_selected:
			funstrings = a.funstrings
	for funstring in funstrings:
		st.latex(funstring)

# plot the attractor in the right column
with col2:
	if option_selected == "Cantor Ternary Set":
		st.pyplot(IFSCatalogue.cantor().plot(n = n, showaxis = True))
	elif option_selected == "Sierpinski Gasket":
		st.pyplot(IFSCatalogue.gasket().plot(n = n, showaxis = True))
	elif option_selected == "Fudgeflake":
		st.pyplot(IFSCatalogue.fudgeflake().plot(n = n, facecolor = 'b', showaxis = True))
	elif option_selected == "Twindragon":
		st.pyplot(IFSCatalogue.twindragon().plot(n = n, facecolor = 'w', showaxis = True))

st.header("Random IFS")

st.write("Under construction.")

st.header("Make your own IFS")

st.write("Under construction.")

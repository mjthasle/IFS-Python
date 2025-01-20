import streamlit as st
from ifs import *
st.set_page_config(layout="wide")
plt.rcParams.update({'font.size': 35})

st.title("Let's draw IFS attractors!")
st.header("Built-in IFS")

multiplot = st.toggle("Multiplot")

if multiplot:
	plt.rcParams['figure.figsize'] = (80, 80)
else:
	plt.rcParams['figure.figsize'] = (16, 16)


col1, col2 = st.columns(2, gap = "large")

# built-in IFS attractors
attractors = get_attractors()
box_options = ["Sierpinski Gasket", "Fudgeflake", "Twindragon"]
box_options = [a.namestring for a in attractors]

def reset_n():
	st.session_state.n = 0


# built-in IFS settings in the left column
with col1:
	option_selected = st.selectbox("Select an IFS attractor to plot",
		box_options, on_change = reset_n)
	if multiplot == False:
		n = st.number_input("Number of iterations: ", min_value = 0, max_value = 8,
			step = 1, key = "n")
	for a in attractors:
		if a.namestring == option_selected:
			funstrings = a.funstrings
	for funstring in funstrings:
		st.latex(funstring)

# plot the attractor in the right column
with col2:
	if multiplot:
		if option_selected == "Cantor Ternary Set":
			start = time.perf_counter()
			st.pyplot(cantor().plot(grid = (1,2)))
			end = time.perf_counter()
		elif option_selected == "Sierpinski Gasket":
			#st.pyplot(gasket().plot(grid = (3,3)))
			start = time.perf_counter()
			gasket().multiplot(grid = (1,2), timeit = True)
			end = time.perf_counter()
		elif option_selected == "Fudgeflake":
			start = time.perf_counter()
			st.pyplot(fudgeflake().plot(grid = (1,2), facecolor = 'b'))
			end = time.perf_counter()
		elif option_selected == "Twindragon":
			start = time.perf_counter()
			st.pyplot(twindragon().plot(grid = (1,2), facecolor = 'w'))
			end = time.perf_counter()
		st.write('Total multiplot time: ' + str(end - start) + ' seconds.')

	else:
		if option_selected == "Cantor Ternary Set":
			st.pyplot(cantor().plot(n = n))
		elif option_selected == "Sierpinski Gasket":
			st.pyplot(gasket().plot(n = n))
		elif option_selected == "Fudgeflake":
			st.pyplot(fudgeflake().plot(n = n, facecolor = 'b'))
		elif option_selected == "Twindragon":
			st.pyplot(twindragon().plot(n = n, facecolor = 'w'))

import streamlit as st
from ifs import *
plt.rcParams.update({'font.size': 22})

st.title("Let's draw IFS attractors!")
st.header("Built-in IFS")
col1, col2 = st.columns(2, gap = "large")

# built-in IFS options
box_options = ["Sierpinski Gasket", "Fudgeflake", "Twindragon"]

def reset_n():
	st.session_state.n = 0

# built-in IFS settings in the left column
with col1:
	option_selected = st.selectbox("Select an IFS attractor to plot", 
		box_options, on_change = reset_n)
	n = st.number_input("Number of iterations: ", min_value = 0, max_value = 10, 
		step = 1, key = "n")
	st.write("IFS:")

# plot the attractor in the right column
with col2:
	if option_selected == "Sierpinski Gasket":
		st.pyplot(gasket().plot(n = n, showaxis = True))  
	elif option_selected == "Fudgeflake":
		st.pyplot(fudgeflake().plot(n = n, facecolor = 'b', showaxis = True))
	elif option_selected == "Twindragon":
		st.pyplot(twindragon().plot(n = n, facecolor = 'w', showaxis = True))

st.header("Random IFS")

st.write("Under construction.")

st.header("Make your own IFS")

st.write("Under construction.")
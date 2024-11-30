import streamlit as st
from ifs import *

st.title("Let's draw IFS attractors!")
st.header("Built-in IFS")
col1, col2 = st.columns(2, gap="large")

# input options
#plt.axis("scaled")
with col1:
	box_options = ["Sierpinski Gasket", "Fudgeflake", "Twindragon"]
	option_selected = st.selectbox("Select an IFS attractor to plot", box_options)
	n = st.number_input("Number of iterations: ", value=0, min_value=0, max_value=10, step=1)

# plot successive iterations in a grid
with col2:
	if option_selected == "Sierpinski Gasket":
		st.pyplot(gasket().plot(n = n))  
	elif option_selected == "Fudgeflake":
		st.pyplot(fudgeflake().plot(n = n, facecolor = 'b'))
	elif option_selected == "Twindragon":
		st.pyplot(twindragon().plot(n = n, facecolor = 'w'))

st.header("Random IFS")

st.write("Under construction.")
import streamlit as st
import matplotlib.pyplot as plt
from ifs import *
plt.rcParams['figure.figsize'] = (5,5)

st.title("Make your own an IFS attractor!")

st.header("Built-in IFS")

# input options
box_options = ["Sierpinski Gasket", "Fudgeflake", "Twindragon"]
option_selected = st.selectbox("Select an IFS attractor to plot", box_options)
n = st.number_input("Number of iterations: ", value=0, min_value=0, max_value=10, step=1)

# plot successive iterations in a grid
if option_selected == "Sierpinski Gasket":
	st.pyplot(gasket().plot(n = n))  
elif option_selected == "Fudgeflake":
	st.pyplot(fudgeflake().plot(n = n, facecolor = 'b'))
elif option_selected == "Twindragon":
	st.pyplot(twindragon().plot(n = n, facecolor = 'w'))

st.header("Random IFS")

st.write("Under construction.")
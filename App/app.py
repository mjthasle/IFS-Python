import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Some Streamlit Examples")

st.header("A Figure")

plt.rcParams['figure.figsize'] = (16,10)

x = np.linspace(0, 1, 200)

y = x

fig, ax = plt.subplots()
ax.plot(x, y)

st.pyplot(fig)

st.header("A Selectbox")

box_options = ["Option 1", "Option 2", "Option 3"]

option_selected = st.selectbox("Which option do you prefer?", box_options)

st.write("Selectbox returns:", option_selected, "of type, type(option_selected)")
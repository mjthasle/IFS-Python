import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (16,10)

x = np.linspace(0, 1, 200)

y = x

fig, ax = plt.subplots()
ax.plot(x, y)

st.pyplot(fig)
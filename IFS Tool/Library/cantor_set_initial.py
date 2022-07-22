import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

x = np.linspace(0, 1, 200)
y = 0*x

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

def f(x, k):
    return (1/3)*x + (2/3)*k

fig, ax = plt.subplots()
ax.plot(x, y)
ax.plot(f(x, 0), y - 0.02)
ax.plot(f(x, 1), y - 0.02)
ax.plot(f(f(x, 0), 0), y - 0.04)
ax.plot(f(f(x, 0), 1), y - 0.04)
ax.plot(f(f(x, 1), 0), y - 0.04)
ax.plot(f(f(x, 1), 1), y - 0.04)
plt.show()
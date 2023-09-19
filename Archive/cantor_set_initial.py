import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams['figure.figsize'] = (16,10)

#Given a positive integer n, codelist returns the list of integers from 0 to 2^n - 1 (inclusive) in binary form, as strings

def codelist(n):
    m = 0
    fns = []
    while m < 2**n:
        fns.append(bin(m)[2:])
        m = m + 1
    return(fns)

#codelist(3)

#normalize takes a list of strings and makes each string the same length by adding zeros on the left of the short ones.

def normalize(x):
    m = 0
    while m <= len(x) - 1:
        if len(x[m]) < len(max(x)):
            while len(x[m]) < len(max(x)):
                x[m] = '0' + x[m]
        else:
            x[m] = x[m]
        m = m + 1
    return x

#normalize(codelist(3))

#Given a string of x_1, x_2,...,x_n of 0s and 1s, the function "iterate" puts the unit interval [0,1] through f(f(f(...f(,x_1),x_2),...,x_n) 

y = 0*x

def f(theta, k):
    return (1/3)*theta + (2/3)*k

def iterate(a):
    x = np.linspace(0, 1, 200)
    for m in np.arange(0, len(a)):
        x = f(x, float(a[m]))
    ax.plot(x, y)
 
#Finally, given an integer n, the function "cantor" plots the nth level of the Cantor set construction

fig, ax = plt.subplots()

def cantor(n):
    for a in normalize(codelist(n)):
        iterate(a)

#As an example, we'll try putting in 4

cantor(4)
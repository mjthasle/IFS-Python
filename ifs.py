# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:23:40 2022

@author: Mitch Haslehurst, Emily Rose Korfanty
"""

# Creates a list of all sequences of length n of numbers between 1 and m
def codes(m, n):
    l = 0
    codes = []
    while l < m**n:
        k = l
        j = n - 1
        expan = []
        while j >= 0:
            expan += [k//(m**j)]
            if k//(m**j) != 0:
                k = k % (m**j)
            j -= 1
        l += 1
        codes += [expan]
    return codes

# Apply the functions in the IFS f in the order of specified by code to the array points
def compose(f, code, points):
    x = points
    for i in code:
        x = f(x, i)
    return x

# Apply all sequences of functions in the IFS f specified by codes to the array points
def iterate(f, codes, points):
    return [compose(f, code, points) for code in codes]




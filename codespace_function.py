#m is the number of functions in the IFS, and n is the number of desired iterations.
#The function codes generates a list of all possible lists of length n consisting of integers from 0 to m - 1.

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
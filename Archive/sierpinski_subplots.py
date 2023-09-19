def f(array, j):
    if j == 0:
        return 0.5*array
    elif j == 1:
        return 0.5*(array + [1, 0])
    else:
        return 0.5*(array + [0.5, np.sqrt(3)/2])

fig, ax = plt.subplots(nrows = 3, ncols = 3)
#ax.set_xlim([0, 1])
#ax.set_ylim([0, 1])

start = time.perf_counter()

for j in range(9):
    points = []
    for code in codes(3, j):
        y = np.array([[0, 0], [1, 0], [0, 1]])    
        for i in code:
            y = f(y, i)
        points += [y]

    for i in points:
        ax[j // 3, j % 3].add_patch(Polygon(i, facecolor = 'k'))
    end = time.perf_counter()
    print('Iteration ' + str(j) + ' took ' + str(end - start) + ' seconds.')
        
plt.show()
end = time.perf_counter()
print('The whole cell took ' + str(end - start) + ' seconds.')
from matplotlib.transforms import Affine2D
import numpy as np
import random

def get_ifs():

	ifs = []
	n = random.randint(2,6)

	for j in range(0,n):
		# Sample elements of matrix and shift uniformly in [0,1)
		matrix = np.random.random((2,2))
		shift = np.random.random((2,1))
		transform = np.concatenate([matrix, shift], axis=1)
		transform=np.concatenate([transform, [[0,0,1]]], axis=0)
		ifs.append(Affine2D(transform))
	return ifs

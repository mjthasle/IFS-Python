from matplotlib.transforms import Affine2D
import numpy as np

def get_ifs():

	ifs = []

	ifs.append(Affine2D().scale(0.5))

	ifs.append(Affine2D().translate(1, 0) + Affine2D().scale(0.5))

	ifs.append(Affine2D().translate(0.5, np.sqrt(3)/2) + Affine2D().scale(0.5))

	return ifs

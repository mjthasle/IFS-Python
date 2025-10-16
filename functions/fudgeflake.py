from matplotlib.transforms import Affine2D
import numpy as np

def get_ifs():

	ifs = []

	ifs.append(Affine2D().rotate(np.pi/6) + Affine2D().scale(1/np.sqrt(3)) +Affine2D().translate(-1/3, 0))

	ifs.append(Affine2D().rotate(np.pi/6) +Affine2D().scale(1/np.sqrt(3)) + Affine2D().translate(0.5*(1/3),(np.sqrt(3)/2)*(1/3)))

	ifs.append(Affine2D().rotate(np.pi/6) + Affine2D().scale(1/np.sqrt(3)) +Affine2D().translate(0.5*(1/3),-(np.sqrt(3)/2)*(1/3)))

	return ifs

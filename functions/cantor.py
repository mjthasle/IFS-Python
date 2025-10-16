from matplotlib.transforms import Affine2D

def get_ifs():

	ifs = []

	ifs.append(Affine2D().scale(1/3))

	ifs.append(Affine2D().translate(2, 0) + Affine2D().scale(1/3))

	return ifs

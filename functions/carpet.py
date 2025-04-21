from matplotlib.transforms import Affine2D

def get_ifs():

	ifs = []

	for i in range(9):
		if i != 4:
			ifs.append(Affine2D().translate(i // 3, i % 3) + Affine2D().scale(1/3))

	return ifs

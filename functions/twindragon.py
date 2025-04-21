from matplotlib.transforms import Affine2D
import numpy as np

def get_ifs():

    ifs = []

    ifs.append(Affine2D().rotate(np.pi/4) +
            Affine2D().translate(-0.5, 0.5) +
            Affine2D().scale(1/np.sqrt(2)))

    ifs.append(Affine2D().rotate(np.pi/4) +
            Affine2D().translate(0.5, -0.5) +
            Affine2D().scale(1/np.sqrt(2)))

    return ifs

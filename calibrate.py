import numpy as np


def focal2distance(x):
    y = 7.0 - (-4.956757e-7/-28.027)*(1 - np.exp(+28.027*x))
    return y

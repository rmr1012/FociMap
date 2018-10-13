import cv2
from matplotlib import pyplot as plt

from huHann import huHann

img = cv2.imread('IMGP2395.JPG')
img=img[:,:,2].astype(int)

blurmap=huHann(img)

plt.imshow(blurmap)
plt.colorbar()
plt.show()

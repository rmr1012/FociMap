import cv2
from matplotlib import pyplot as plt
import os
from huHann import huHann

#img = cv2.imread('IMGP2395.JPG')
#img=img[:,:,2].astype(int)
for filename in os.listdir("phoneSet"):
	print(filename)
	im = cv2.imread('phoneSet/'+filename)
	img=im[:,:,2].astype(int)
	blurmap=huHann(img)
	plt.subplot(1,2,1)
	plt.imshow(im)
	plt.subplot(1,2,2)
	plt.imshow(blurmap,cmap='gray')
	plt.colorbar()
	plt.savefig("phoneSet/HH"+filename[:-4]+".png")
	plt.close()

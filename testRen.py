import matplotlib
from matplotlib import pyplot as plt
from ren import renAlgo
import numpy as np

files=["6.JPG","7.JPG","8.JPG","9.JPG","10.JPG","11.JPG","12.JPG"]
focal=[6     , 12.  ,   18,    24,     36,     72,       200]

filesDir=[]
for file in files:
    filesDir.append("stitch/"+file)

smoothDepth=renAlgo(filesDir,focal)


plt.imshow(smoothDepth,norm=matplotlib.colors.LogNorm(),cmap='gray')
plt.colorbar()
plt.show()

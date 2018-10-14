
import matplotlib
from matplotlib import pyplot as plt
from ren import renAlgo
import numpy as np
import os
from calibrate import focal2distance
import pickle
import sys

def crunchData(folder,outfile):
    focal=[0.4, 0.55, 0.7, 0.72, 0.75, 0.77, 0.8, 0.85]
    #focal=[focal2distance(x) for x in focal]
    print(focal)
    filesDir=[]
    for file in os.listdir(folder):
        filesDir.append(folder+"/"+file)

    print(len(focal))
    print(len(filesDir))
    print("starting Ren Algo")
    smoothDepth=renAlgo(filesDir,focal)
    print("finished Ren Algo, saving")
    plt.imshow(smoothDepth,cmap='gray')
    plt.colorbar()
    pickle.dump(smoothDepth, open( "smoothDepth.p", "wb" ) )

    plt.imsave(outfile,smoothDepth,cmap='gray')

if __name__=="__main__":
    folder=sys.argv[1]
    outfile=sys.argv[2]
    crunchData(folder,outfile)

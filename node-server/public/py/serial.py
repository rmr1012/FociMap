
import matplotlib
from matplotlib import pyplot as plt
from ren import renAlgo
import numpy as np
import os
#from calibrate import focal2distance
import pickle
import sys
import cv2
from huHann import huHann
import scipy
import scipy.signal as sig
import json
def neighbourReplace(src,size):
    Rf=scipy.ndimage.maximum_filter(src,size=size)
    src[np.where(src<=0.49)]= Rf[np.where(src<=0.49)]
    return src
def crunchSerial(inSer,outfile):
    print("serial processing")
    print("inSer",inSer)
    print("outfile",outfile)
#    jsonData=json.loads(open(inJson,"r").read())
#    jsonData=jsonData["fileset"]
    focal=[0.5, 0.6, .7, .75, .8, .85, .9, .95]
    filepaths=["public/images/"+str(inSer)+"_"+str(ind) for ind in range(8) ]
    confMaps=[]
    for ohPath in filepaths:
         confMaps.append(pickle.load(open(ohPath+".jpg.p","rb")))

    flatConf=np.array(confMaps)

    semiFlatConf=np.array(confMaps)
    flatConf=semiFlatConf.reshape(semiFlatConf.shape[0],-1)
    print(flatConf.shape)
    max_idx=flatConf.argmax(0)
    print(max_idx)
    depth_1d=np.array(list(map(lambda x: focal[x],max_idx)))
    oneDepth=depth_1d.reshape(semiFlatConf.shape[1],semiFlatConf.shape[2])

    normDep=255*(oneDepth-min(focal))/(max(focal)-min(focal))
    result=neighbourReplace(normDep,100)    
# and renormalize

    print("finished Ren Algo, saving")
    # plt.imshow(smoothDepth,cmap='gray')
    # plt.colorbar()
    # pickle.dump(smoothDepth, open( "smoothDepth.p", "wb" ) )

    plt.imsave(outfile,result,cmap='gray')


if __name__=="__main__":
    inSer=sys.argv[1]
    outFile=sys.argv[2]
    
    crunchSerial(inSer,outFile)

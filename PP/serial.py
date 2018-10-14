
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
def crunchSerial(inJson,outfile):
    print("serial processing")
    jsonData=json.loads(open(inJson,"r").read())
    jsonData=jsonData["masterList"]
    focal=[]
    confMaps=[]
    for item in jsonData:
        focal.append(item["focal"])
        confMaps.append(pickle.load(open(item["filename"]+".p","rb")))

#    flatConf=np.array(confMaps)

    semiFlatConf=np.array(confMaps)
    flatConf=semiFlatConf.reshape(semiFlatConf.shape[0],-1)
    print(flatConf.shape)
    max_idx=flatConf.argmax(0)
    print(max_idx)
    depth_1d=np.array(list(map(lambda x: focal[x],max_idx)))
    oneDepth=depth_1d.reshape(semiFlatConf.shape[1],semiFlatConf.shape[2])

    result=255*(neighbourReplace(oneDepth,100)-min(focal))/(max(focal)-min(focal))
    # and renormalize

    print("finished Ren Algo, saving")
    # plt.imshow(smoothDepth,cmap='gray')
    # plt.colorbar()
    # pickle.dump(smoothDepth, open( "smoothDepth.p", "wb" ) )

    plt.imsave(outfile,result,cmap='gray')


if __name__=="__main__":
    inJson=sys.argv[1]
    outFile=sys.argv[2]

    crunchSerial(inJson,outFile)


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

    flatConf=np.array(confMaps)

    oneDepth=np.ones([len(flatConf[0,:,0]),len(flatConf[0,0,:])])
    for row in range(len(flatConf[0,:,0])):
        for col in range(len(flatConf[0,0,:])):
            corr=flatConf[:,row,col]
            maxInd=corr.argmax()
            #print(maxInd)
            oneDepth[row,col]=focal[maxInd]

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

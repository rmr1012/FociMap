import copy
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
    focal=[0.6, 0.65, 0.70, 0.72, 0.75, 0.78, 0.8, 0.95]
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

    normalize=255*(oneDepth-min(focal))/(max(focal)-min(focal))
    mu=  cv2.blur(normalize, (100,100))
    mu2= cv2.blur(np.multiply(normalize,normalize), (100,100));
    sigma=cv2.sqrt(np.abs(mu2 - np.multiply(mu,mu)))
    #bisigma=copy.copy(sigma)
    tresh=sigma.max()*0.45
    fatblur=cv2.blur(normalize, (500,500))
    normalize[np.where(sigma>tresh)]= fatblur[np.where(sigma>tresh)]

    normalize=255-normalize
    mu=  cv2.blur(normalize, (50,50))
    mu2= cv2.blur(np.multiply(normalize,normalize), (50,50));
    sigma=cv2.sqrt(np.abs(mu2 - np.multiply(mu,mu)))
    #bisigma=copy.copy(sigma)
    tresh=sigma.max()*0.45
    fatblur=cv2.blur(normalize, (500,500))
    normalize[np.where(sigma>tresh)]= fatblur[np.where(sigma>tresh)]

    normalize=255-normalize
    eqed=cv2.equalizeHist(normalize.astype(np.uint8))

    result=eqed#cv2.blur(eqed,(25,25))

#    normDep=255*(oneDepth-min(focal))/(max(focal)-min(focal))
 #   result=neighbourReplace(normDep,100)    
# and renormalize

    print("finished Ren Algo, saving")
    # plt.imshow(smoothDepth,cmap='gray')
    # plt.colorbar()
    # pickle.dump(smoothDepth, open( "smoothDepth.p", "wb" ) )
    cmd=("cp public/images/"+str(inSer)+"_6.jpg public/images/"+str(inSer)+".jpg")
    print(cmd)
    os.system(cmd)
    for ohPath in filepaths:
        try:
            os.remove(ohPath+".jpg.p")
            os.remove(ohPath+".jpg")
        except:
            pass
    plt.imsave(outfile,result,cmap='gray')


if __name__=="__main__":
    inSer=sys.argv[1]
    outFile=sys.argv[2]
    
    crunchSerial(inSer,outFile)

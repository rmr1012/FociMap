
import cv2
import matplotlib
from matplotlib import pyplot as plt
import os
from huHann import huHann
import scipy
import scipy.signal as sig
import numpy as np
#import pickle

def neighbourReplace(src,size):
    Rf=scipy.ndimage.maximum_filter(src,size=size)
    src[np.where(src<=0.49)]= Rf[np.where(src<=0.49)]
    return src

def renAlgo(files,focal):
    confMaps=[]
    for index, filename in enumerate(files):
        print(filename)
        im = cv2.imread(filename)
        img=im[:,:,2].astype(int)
        blurmap=huHann(img)
        nmap=(8-blurmap)/8
        blur = cv2.GaussianBlur(nmap,(99,99),0)
        blur = cv2.GaussianBlur(blur,(99,99),0) # second order
        confMaps.append(blur)

    flatConf=np.array(confMaps)

    oneDepth=np.ones([len(flatConf[0,:,0]),len(flatConf[0,0,:])])*999
    for row in range(len(flatConf[0,:,0])):
        for col in range(len(flatConf[0,0,:])):
            corr=flatConf[:,row,col]
            maxInd=corr.argmax()
            #print(maxInd)
            oneDepth[row,col]=focal[maxInd]

    result=255*(neighbourReplace(oneDepth,100)-min(focal))/(max(focal)-min(focal))
    # and renormalize
    return result

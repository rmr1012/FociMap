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


def crunchParallel(filename):

    print("parallel processing "+filename)
    im = cv2.imread(filename)
    img=im[:,:,2].astype(int)
    #blurmap=huHann(img)
    nmap=(8-huHann(img))/8
    blur = cv2.GaussianBlur(nmap,(99,99),0)
    blur = cv2.GaussianBlur(blur,(99,99),0) # second order

    pickle.dump(blur, open( theFile+".p", "wb" ) )


if __name__=="__main__":
    theFile=sys.argv[1]

    crunchParallel(theFile)
    print("done")

import numpy as np
from numpy import inf, nan
from cv2 import filter2D
import scipy.ndimage

def matlab_style_gauss2D(shape,sigma):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def huHann(img): # input 2d image

    #print("step 0")

    #print("step 1")
    sigmaA=8
    sigmaB=10
    #print("step 2")
    sigmaMax=max(sigmaA,sigmaB)
    fsz=[sigmaMax, sigmaMax] # function size
    #print("step 3")
    kernelA=matlab_style_gauss2D(fsz,sigmaA)
    kernelB=matlab_style_gauss2D(fsz,sigmaB)
    #print("step 4")
    imgA=filter2D(img,-1,kernelA)
    imgB=filter2D(img,-1,kernelB)
    #print("step 5")
    R1=np.subtract(img,imgA)
    R2=np.subtract(imgA,imgB)
    #print("step 6")
    #print("step 7")
    R=np.divide(R1,R2)
    R[R == -inf] = 0
    R[R == inf] = 0
    R=np.nan_to_num(R)
    #print("step 8")
    Rf=scipy.ndimage.maximum_filter(R,size=8)
    #print("step 9")
    blurmap=np.divide((np.multiply(sigmaA,sigmaB)),(np.multiply((sigmaB-sigmaA),Rf)+sigmaB))
    #print("step 10")
    return blurmap

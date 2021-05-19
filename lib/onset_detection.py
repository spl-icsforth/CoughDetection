
import numpy as np

def onset_detection(aux,sampleIdxs,frameEn,Fs,detectParams):
  
    aux[0]=1;
    sJump=detectParams['hopSize']
    detectDifference=np.ceil(detectParams['minOnsetDiff']*Fs)
    N=np.shape(aux)[0]
    lastPeak=-np.inf
    onsetSamples=np.zeros((0,1),dtype=int)
    onsetPoints=np.zeros((0,1),dtype=int)
    onsetEnergy=np.zeros((0,1),dtype=float)

    for i in range(0,N):
        if (i-lastPeak)*sJump > detectDifference and \
            aux[i] >= detectParams['treshold'] and \
                frameEn[i] > detectParams['energyThreshold']:
           onsetSamples=np.append(onsetSamples,sampleIdxs[i])
           onsetPoints=np.append(onsetPoints,i)
           onsetEnergy=np.append(onsetEnergy,frameEn[i])
           lastPeak=i

    return onsetSamples.astype(int), onsetPoints.astype(int), onsetEnergy  

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:58:31 2019
attemp to modify onset reduction so that it gives a higher value at broadband onsets than at
narrowband onsets. Vlepe onset_reduction_cough in EDK/cough in Matlab
@author: nstefana
"""
import numpy as np

def onset_reduction_cough(s,Fs,detectParams):

    hopSize=detectParams['hopSize']
    Ns=np.shape(s)[0]
    NsFrame = int(np.round(detectParams['frameDuration']*Fs))
    # Enforce evenness of the frame's length
    NsFrame = int(np.round(NsFrame/2)) * 2 
    halfDur = int(np.round(NsFrame/2))
    ffAll=np.arange(0,NsFrame,1,dtype=float)*Fs/NsFrame
    lowFreqIdx=np.argmin(np.abs(ffAll-detectParams['freqLimits'][0]))
    highFreqIdx=np.argmin(np.abs(ffAll-detectParams['freqLimits'][1]))
    ffUse=np.arange(lowFreqIdx,highFreqIdx)
    previousFreqResponse=(10**9)*np.ones((ffUse.size,),dtype=float);
    

    hanwin=np.hanning(NsFrame)
    sampleIdxs=np.arange(halfDur,Ns-halfDur,hopSize,dtype=int)  
    N = len(sampleIdxs)
    frameOutput=np.zeros(N,dtype=float)
    frameEn=np.zeros(N,dtype=float)
    for n in range(0,N):
        frameIN = s[sampleIdxs[n]-halfDur:sampleIdxs[n]+halfDur]#-1]
        frameIN=np.multiply(frameIN,hanwin)
        fftFrame=np.fft.fft(frameIN,n=NsFrame,axis=0)
        tmp = np.abs(fftFrame)/NsFrame
        freqResponse=tmp[lowFreqIdx:highFreqIdx]
        frameEn[n]=np.sum(freqResponse)
#        if n>1:
#            frameEn[n-1]=np.max((frameEn[n-1],frameEn[n]))
            
        freqEnergyRatio=np.log2(np.divide(freqResponse,previousFreqResponse))
        binaryRatio=(freqEnergyRatio>detectParams['percTresh'])
        previousFreqResponse=freqResponse
        accum=0
        for u in range(1,ffUse.size-1):
            if binaryRatio[u]:
                if np.any([binaryRatio[u-1], binaryRatio[u+1]]):
                    accum=accum+1
        frameOutput[n]=accum            
#        frameOutput[n]=np.sum(binaryRatio)
    ## Create window matrix and apply to frames
    return frameOutput, sampleIdxs, frameEn
    
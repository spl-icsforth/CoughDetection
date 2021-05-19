
import numpy as np
import audioread
import librosa
import soundfile as sf 
from queue import Queue
from threading import Thread 
from onset_reduction_cough import onset_reduction_cough 
from onset_detection import onset_detection
from librosa.feature import melspectrogram
import os

class ClipCoughDetector:
    ''' Object for extracting onsets and using the pretrained DNN in order to
    detect cough sounds. You can change the hardcoded parameter values in the 
    classes constructor'''
    
    def __init__(self,model):
        self.worker_finished = False
        self.model = model
        self.results_list = []
        #onset detection setup
        
        #maximum duration per segment, if a clip is larger than maxDur it will
        #be split into segments of maxDur seconds each
        self.maxDur = 600 
        self.Fs = 16000
        self.segmDuration = int(0.5 * 16000)
        self.offset = 2000
        
        self.detectParams={'hopSize':512, 'freqLimits':(120, 6000),
                           'minOnsetDiff':0.12,'frameDuration':0.042, 
                           'treshold':77, 'percTresh':1.9,
                           'energyThreshold':0.015}
        self.frameLength_mel = int(0.04 * self.Fs) #0.020 default
        self.stride_mel = int(0.02 * self.Fs)
        self.numFilters_mel = 128 
        self.fftLength_mel = 1024  
        #number of time frames
        self.Nframes = 29
        self.useFeatures = np.arange(0,128) 
        self.Nf = len(self.useFeatures)
        self.audioPathFolder='CoughResults'
        
    def reset(self):
        self.results_list = []
        self.worker_finished = False
        self.featMatrix = np.zeros((0,self.Nframes,self.numFilters_mel), 
                                   dtype=np.float32)
        self.coughDetections = np.zeros((0,3),dtype=np.float16)
        self.audioOUT = np.zeros((0,),dtype=float)
        self.audioOUT_other = np.zeros((0,),dtype=float)
        self.Ncoughs = 0
        self.Nothers = 0
        self.wav_path = ''
        
    def unfoldResults(self):
        for (audioOUT_temp,coughDetections_temp) in self.results_list:
            if audioOUT_temp.size != 0:
                self.audioOUT = np.append(
                    self.audioOUT,np.append(np.zeros((2000,1),dtype=float),
                                       audioOUT_temp), axis=0)
                self.coughDetections = np.append(self.coughDetections,
                                             coughDetections_temp, axis = 0)
    def getClipCoughs(self,wav_path,n_threads_to_use):
        self.reset()
        self.wav_path = os.path.abspath(wav_path)
        # self.wav_path = self.wav_path.replace("\\", "/")
        # self.wav_path = wav_path.replace("", "/")
        
        with audioread.audio_open(wav_path) as f:
            print(f.channels, f.samplerate, f.duration)
          
        if f.duration < self.maxDur:
            self.timeBorders = np.array((0,f.duration))   
        else:
            self.timeBorders = np.arange(0,f.duration,self.maxDur)
            self.timeBorders = np.delete(self.timeBorders,-1,axis = None)
            self.timeBorders = np.append(self.timeBorders,f.duration)
            
        self.Nsegm = self.timeBorders.size 
        #in case that number of segments is less than n_threads
        n_threads_to_use = min(n_threads_to_use,self.Nsegm)
        work_q = Queue()# no limit at the que
        worker_list = []
        for i in range(n_threads_to_use):
            worker = Thread(target = self.getOnsetsOfSegment,args = (work_q,))
            worker.setDaemon(True)
            worker.start()
            worker_list.append(worker)
        
        for segm_n in range(0,self.Nsegm - 1):
            work_q.put(segm_n)    
        work_q.join() #block    
        self.worker_finished = True
        for i in range(n_threads_to_use):	
            worker_list[i].join()
        
        self.unfoldResults()
        # wav_name = wav_path.split('/')[-1][:-4]   
        wav_name = os.path.basename(wav_path)
        print('wav name is',self.wav_path)
        
        for result in self.results_list:
            self.Ncoughs += len(result[1])
        
        if self.Ncoughs > 0:
            results_wav_path = os.path.join(
                os.getcwd(),
                self.audioPathFolder,
                wav_name + '_coughDetections.wav')
                
            sf.write((
                results_wav_path),
                     self.audioOUT,self.Fs)
            results_text_path = os.path.join(
                os.getcwd(),
                self.audioPathFolder,
                wav_name + '_coughDetections.txt')
            np.savetxt(
                results_text_path, 
                self.coughDetections,
                fmt = '%4.3f', 
                delimiter = '  ', 
                header = ('Idx | Time (s) | Confidence'))
            print(self.coughDetections)     
            print(self.Ncoughs, ' coughs found in',self.wav_path)
        else :
            print('No coughs found in ', self.wav_path)
                  
    def getOnsetsOfSegment(self,work_q):
        while not self.worker_finished:
            try:
                segment_n = work_q.get(timeout=0.1)
            except:
                continue
            
            #lists needed for batched implementation (reset for each segment)
            featureIN_list = []
            eventLocation_list = []
            confidence_list = []
            sigIN_list = []
            cl_list = []
            
            audioOUT = np.zeros((0,),dtype=float)
            coughDetections = np.zeros((0,3),dtype=np.float16)
            tStart = self.timeBorders[segment_n]
            tEnd = self.timeBorders[segment_n + 1]
            segmDur = tEnd - tStart
            
            sIN,_ = librosa.load(
                self.wav_path, sr = self.Fs, 
                offset = tStart,
                duration=segmDur)
            
            auxi,sampleIdxs,frameEn = onset_reduction_cough(
                sIN,self.Fs,
                self.detectParams)
            detectParams = self.detectParams.copy()
            detectParams['energyThreshold'] = 0.08 * np.max(frameEn)
            onsetSamples,onsetPoints,onsetEnergy = onset_detection(
                auxi,
                sampleIdxs,
                frameEn,
                self.Fs,
                detectParams)
            Ns = len(sIN)
            onset_Flag = False
            for o in onsetSamples:   
                if  Ns-o > self.segmDuration and o > self.offset:
                    sigIN = sIN[o - self.offset:o + self.segmDuration] 
                    sigIN = sigIN / np.linalg.norm(sigIN) 
                    eventLocation_list.append((tStart + float(o / self.Fs)))
                    #flag is set to True if at least one valid onset is found
                    onset_Flag = True
                else:
                    eventLocation_list.append(None)
                    continue
                sigIN_list.append(sigIN)
                melsIN = melspectrogram(
                    sigIN,sr = self.Fs,
                    S = None,
                    n_mels = self.numFilters_mel,
                    n_fft = self.fftLength_mel,
                    hop_length = self.stride_mel,
                    window = 'hann',
                    win_length = self.frameLength_mel,
                    center = False, 
                    power = 2.0)
                melsIN = np.transpose(melsIN)
                melsIN = np.log10(
                    melsIN[0:self.Nframes,
                    self.useFeatures]+10**(-6)*np.ones((self.Nframes,self.Nf)))
                featureIN_list.append(melsIN)
                
            #in case that no valid onset is found
            if onset_Flag:
                prediction_list = self.model.predict(
                    np.asarray(featureIN_list,dtype = 'float32'))
                cl_list = np.argmax(prediction_list,axis = 1)
                Ncoughs = 0
                
                confidence_list = np.max(prediction_list,axis = 1)
                for onset_idx,cl in enumerate(cl_list):
                    if cl == 1:
                        Ncoughs += 1
                        dataIN=np.reshape(
                            np.array((
                                Ncoughs,
                                eventLocation_list[onset_idx],
                                confidence_list[onset_idx])
                            ,dtype=np.float16),
                            (1,3))
                        coughDetections=np.append(
                            coughDetections,
                            dataIN,
                            axis = 0)
                        audioOUT=np.append(
                            audioOUT,
                            np.append(
                                np.zeros(
                                    (2000,1),
                                    dtype = float),
                                sigIN_list[onset_idx]), 
                            axis=0)
            self.results_list.append((audioOUT,coughDetections))
            work_q.task_done()       
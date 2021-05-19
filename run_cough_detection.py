
import os
import argparse
from tensorflow.keras.models import load_model
from pathlib import Path
import time
import sys
sys.path.append("./lib/")
from ClipCoughDetector import ClipCoughDetector

''' Given as input a folder, this script searches for .wav files for cough 
instances. If a recording is long enough (more than maxDur) it will be process
ed by multiple threads simultaneously.

Parameters:
    -t (int): Maximum number of threads used
                
Output:
     Folder named `CoughDetections` is created and all results are stored there.
     For each `.wav` file, if one or more coughs are detected:
        1) A `.txt` file will be exported which contains each cough instance's 
        timestamp as well as the corresponding level of confidence the 
        classifier has. 
        
        2) Additionaly a `.wav` file containing all the cough detections 
        concatenated, is exported

Syntax examples: 
    python run_cough_detection.py path/that/points/to/folder/with/wavs 
    python run_cough_detection.py path/that/points/to/folder/with/wavs -t 16
  
'''

def main():
    parser = argparse.ArgumentParser(
        description='batch_processor', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('pathIN', help = 'folder containing audio data')    
    parser.add_argument('-t', '--nThreads', type=int, default=4, 
                        help = 'maximum number of threads to use')    
      
    args = parser.parse_args()
    wav_folder = args.pathIN
    n_threads_to_use = args.nThreads
    print('Using a maximum of',n_threads_to_use,' threads')
    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # force to use cpu
    os.makedirs("CoughResults", exist_ok = True) 
    wav_path_list = [
        str(wav_path) for wav_path in Path(wav_folder).rglob('*.wav')]
    
    model = load_model('./lib/models/rnn_mel_entire.hdf5')
    timeStart = time.time()
    cough_detector = ClipCoughDetector(model)
      	
    for wav_path in wav_path_list:
       cough_detector.getClipCoughs(wav_path,n_threads_to_use)
    
    print('Elapsed time: ',time.time()-timeStart,' seconds')

if __name__ == "__main__":
    main() 
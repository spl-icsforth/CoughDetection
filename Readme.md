# A Universal System for Cough Detection in Domestic Acoustic Environments
 **Nikonas Simou¹,Nikolaos Stefanakis¹², Konstantinos Psaroulakis¹**
> **¹** FORTH-ICS, Heraklion, Crete, Greece, GR-70013
> **²** Hellenic Mediterranean University, Department of Music Technology and Acoustics, Rethymno, Greece, GR-74100

-----
## Initial setup 
1) Extract the folder containing the source files in any directory of your hard drive.
2) Install [anaconda], by downloading the installer from the official website. (e.g. Anaconda3-2020.02-Windows-x86_64.exe).
After installation, "anaconda prompt" will show up in the program list.
3) Open anaconda prompt and navigate to the folder which contains the code. (e.g. by typing "cd D:/MyDocuments/CoughDetection")
4) In Anaconda prompt type:
    ```sh
    pip install -r requirements.txt
    ```
    in order to install all required libraries.
    This might take some time but it is important for this procedure to be completed 
    successfully.
-----
## Running the algorithm on your data
The system should be ready to run by now. You can run the tool by calling "run_cough_detection.py" function.
1) Open anaconda prompt and navigate to the source code.
2a) Run the command line version by passing as argument the path of the folder which contains the recordings to be analyzed.
For example, if the path is "D:/audio/saw_recordings/RP10", then we can simply type (in anaconda prompt):
    ```sh
    python run_cough_detection.py D:/audio/domestic_recordings/
    ```
* The path of the folder which contains the recordings is the only mandatory input argument.
* An additional parameter is:

	* **Number of threads** to be used. For example, if we want to engage 8 threads, we can type:
        ```sh
        python run_cough_detection.py D:/audio/domestic_recordings/ -t 8
        ```
2b) Run the graphical version of the tool to configure the wav folder and the number of threads by running: 
		```sh
        python run_cough_detection_gui.py
        ```
	After clicking "Run", GUI will disappear and execution continues on command prompt.

## OUTPUT 
A folder named `CoughDetections` is created and all results are stored there. For each `.wav` file in the input folder, if one or more coughs are detected:
1) A `.txt` file will be exported which contains each cough instance's timestamp as well as the corresponding level of confidence the classifier has. 
2) Additionaly a `.wav` file containing all the cough detections concatenated, is exported.	        
-----	  

## License
MIT 

Copyright (c) 2021 **Nikonas Simou, Nikolaos Stefanakis, Konstantinos Psaroulakis**

--------
### How to reference
If you find any of this library useful for your research, please give cite as:
Nikonas Simou; Nikolaos Stefanakis; Panagiotis Zervas, ["A Universal System for Cough Detection in Domestic Acoustic Environments"](https://ieeexplore.ieee.org/document/9287659) in EUSIPCO 2020.


#### Important notes:
1) Tool converts recordings to 16kHz.

2) For long-duration recordings, the tool is configured to use multiple threads. Each thread handles a `maxDur` seconds segment.
The default value for `maxDur` is set to 600 seconds.

3) You can change the onset detector parameters by tweaking the hardcoded values located in the `ClipCoughDetector` class.


 [anaconda]: <https://anaconda.org/>

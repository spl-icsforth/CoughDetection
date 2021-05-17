# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coughv2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

citation = 'Nikonas Simou; Nikolaos Stefanakis; Panagiotis Zervas, "A Universal System for Cough Detection in Domestic Acoustic Environments" in EUSIPCO 2020.'

def main(wav_folder, n_threads_to_use=4):

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
'''
    import os
    import argparse
    from tensorflow.keras.models import load_model
    from pathlib import Path
    import time
    from ClipCoughDetector import ClipCoughDetector
    
    print('Using a maximum of',n_threads_to_use,' threads')
    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # force to use cpu
    os.makedirs("CoughResults", exist_ok = True) 
    wav_path_list = [
        str(wav_path) for wav_path in Path(wav_folder).rglob('*.wav')]
    
    model = load_model('./rnn_mel_entire.hdf5')
    timeStart = time.time()
    cough_detector = ClipCoughDetector(model)
        
    for wav_path in wav_path_list:
       cough_detector.getClipCoughs(wav_path,n_threads_to_use)
    
    print('Elapsed time: ',time.time()-timeStart,' seconds')




class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(530, 551)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 531, 551))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(9, 3, 159, 255), stop:1 rgba(3, 0, 76, 255));\n"
"\n"
"border-radius: 10px\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_run = QtWidgets.QPushButton(self.frame)
        self.btn_run.setGeometry(QtCore.QRect(150, 430, 221, 91))
        self.btn_run.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(88, 255, 107, 150);\n"
"}")
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self.run_main)

        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 80, 511, 341))
        self.frame_2.setStyleSheet("background-color: rgb(227, 227, 227);border-radius:10px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.btn_dir = QtWidgets.QPushButton(self.frame_2)
        self.btn_dir.setGeometry(QtCore.QRect(20, 10, 151, 61))
        self.btn_dir.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(85, 255, 127, 150);\n"
"}")
        self.btn_dir.setObjectName("btn_dir")
        self.btn_dir.clicked.connect(self.select_dir)

        self.wav_folder = QtWidgets.QTextBrowser(self.frame_2)
        self.wav_folder.setGeometry(QtCore.QRect(26, 100, 271, 51))
        self.wav_folder.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wav_folder.setObjectName("wav_folder")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(350, 70, 141, 31))
        self.label_2.setObjectName("label_2")
        self.wavs = QtWidgets.QTextBrowser(self.frame_2)
        self.wavs.setGeometry(QtCore.QRect(26, 180, 271, 121))
        self.wavs.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wavs.setObjectName("wavs")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(30, 80, 151, 16))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(26, 160, 151, 16))
        self.label_3.setObjectName("label_3")
        self.num_of_threads = QtWidgets.QSpinBox(self.frame_2)
        self.num_of_threads.setGeometry(QtCore.QRect(360, 110, 91, 41))
        self.num_of_threads.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.num_of_threads.setMinimum(1)
        self.num_of_threads.setMaximum(20)
        self.num_of_threads.setObjectName("num_of_threads")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(146, 34, 241, 41))
        self.textBrowser.setStyleSheet("background-color: rgb(221, 249, 249)")
        self.textBrowser.setObjectName("textBrowser")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 531, 31))
        self.frame_3.setStyleSheet("background-color: rgb(101, 0, 152);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
#         self.btn_max = QtWidgets.QPushButton(self.frame_3)
#         self.btn_max.setGeometry(QtCore.QRect(460, 10, 21, 16))
#         self.btn_max.setStyleSheet("QPushButton{ \n"
# "border:none; \n"
# "border-radius: 7px; \n"
# "background-color: rgb(200, 130, 0);\n"
# "}\n"
# "QPushButton:hover{\n"
# "background-color: rgb(200, 130, 0, 150);\n"
# "}")
#         self.btn_max.setText("")
#         self.btn_max.setObjectName("btn_max")
#         self.btn_min = QtWidgets.QPushButton(self.frame_3)
#         self.btn_min.setGeometry(QtCore.QRect(430, 10, 21, 16))
#         self.btn_min.setStyleSheet("QPushButton{ \n"
# "border:none; \n"
# "border-radius: 7px; \n"
# "background-color: rgb(85, 255, 127);\n"
# "}\n"
# "QPushButton:hover{\n"
# "background-color: rgb(85, 255, 127, 150);\n"
# "}")
#         self.btn_min.setText("")
#         self.btn_min.setObjectName("btn_min")
        self.btn_exit = QtWidgets.QPushButton(self.frame_3)
        self.btn_exit.setGeometry(QtCore.QRect(490, 10, 21, 16))
        self.btn_exit.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(235, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(235,0,0, 150);\n"
"}")
        self.btn_exit.setText("")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(self.on_closing)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_run.setText(_translate("MainWindow", "RUN"))
        self.btn_dir.setText(_translate("MainWindow", "Select\n"
"Directory"))
        self.wav_folder.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">[Please select a directory]</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Number of threads:"))
        self.wavs.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">[No directory selected]</p></body></html>"))
        self.label.setText(_translate("MainWindow", "Directory with wav files:"))
        self.label_3.setText(_translate("MainWindow", "Files to be processed:"))

    def select_dir(self):
        import glob
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            self.wav_folder.setText(folder)
            files = glob.glob(f"{folder}/**/*.wav", recursive=True)
            if len(files)>0:
                files = "\n".join(files).replace("\\", "/").replace(folder, "./")
                files = "Files to be processed:\n"+files
                self.btn_run.setEnabled(True)
                self.btn_run.setText("RUN")
            else:
                files = "Files to be processed:\n"+"No .wav files found in selected directory."
                self.btn_run.setText("RUN\nSelect a valid directory.")
                self.btn_run.setEnabled(False)
            self.wavs.setText(files)
        #window.label_2.setText(file)


    def on_closing(self):
        import gc

        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtWidgets.QMessageBox.Yes | 
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            print('Thank you for using our tool!')
            QtCore.QCoreApplication.instance().quit()
            gc.collect()
            exit()


        # if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):



    # def copy_citation(self):
    #     self.parent.clipboard_clear()
    #     self.parent.clipboard_append(citation)
    #     self.parent.update() # the text will stay there after the window is closed
    #     self.copied_lbl_txt.set("(Copied!)")
        
    def run_main(self):
        global wav_folder, n_threads_to_use
        wav_folder = self.wav_folder.toPlainText()
        n_threads_to_use = int(self.num_of_threads.value())
        QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec()
    MainWindow.close()
    print("Starting execution. Please wait...")
    main(wav_folder, n_threads_to_use)


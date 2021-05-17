# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coughv2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore
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
        MainWindow.resize(530, 610)
        MainWindow.setFixedSize(self.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 531, 611))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(9, 3, 159, 255), stop:1 rgba(3, 0, 76, 255));\n"
"\n"
"border-radius: 10px\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_run = QtWidgets.QPushButton(self.frame)
        self.btn_run.setGeometry(QtCore.QRect(156, 420, 220, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_run.setFont(font)
        self.btn_run.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(88, 255, 107, 150);\n"
"}")
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self.run_main)

        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 60, 511, 341))
        self.frame_2.setStyleSheet("background-color: rgb(227, 227, 227);border-radius:10px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.btn_dir = QtWidgets.QPushButton(self.frame_2)
        self.btn_dir.setGeometry(QtCore.QRect(90, 10, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_dir.setFont(font)
        self.btn_dir.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(85, 255, 127, 150);\n"
"}")
        self.btn_dir.setObjectName("btn_dir")
        self.btn_dir.clicked.connect(self.select_dir)        
        self.wav_folder = QtWidgets.QTextBrowser(self.frame_2)
        self.wav_folder.setGeometry(QtCore.QRect(26, 100, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.wav_folder.setFont(font)
        self.wav_folder.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wav_folder.setObjectName("wav_folder")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(360, 70, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.wavs = QtWidgets.QTextBrowser(self.frame_2)
        self.wavs.setGeometry(QtCore.QRect(26, 180, 271, 121))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.wavs.setFont(font)
        self.wavs.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wavs.setObjectName("wavs")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(30, 80, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(26, 160, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.num_of_threads = QtWidgets.QSpinBox(self.frame_2)
        self.num_of_threads.setGeometry(QtCore.QRect(360, 110, 91, 41))
        self.num_of_threads.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.num_of_threads.setMinimum(1)
        self.num_of_threads.setMaximum(20)
        self.num_of_threads.setObjectName("num_of_threads")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 530, 30))
        self.frame_3.setStyleSheet("background-color: rgb(101, 0, 152);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.btn_min = QtWidgets.QPushButton(self.frame_3)
        self.btn_min.setGeometry(QtCore.QRect(470, 5, 20, 20))
        self.btn_min.clicked.connect(self.minimize)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_min.setFont(font)
        self.btn_min.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(235, 157, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(235, 157, 0, 150);\n"
"}")
        self.btn_min.setObjectName("btn_min")
        self.btn_exit = QtWidgets.QPushButton(self.frame_3)
        self.btn_exit.setGeometry(QtCore.QRect(500, 5, 20, 20))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_exit.setFont(font)
        self.btn_exit.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(235, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(235,0,0, 150);\n"
"}")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(self.on_closing)

        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(11, -3, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.copy_citation = QtWidgets.QPushButton(self.frame)
        self.copy_citation.setGeometry(QtCore.QRect(400, 570, 101, 21))
        self.copy_citation.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(200, 130, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(200, 130, 0, 150);\n"
"}")
        self.copy_citation.setObjectName("copy_citation")
        self.copy_citation.clicked.connect(self.copy_citation_)
        self.cite_label = QtWidgets.QPlainTextEdit(self.frame)
        self.cite_label.setGeometry(QtCore.QRect(20, 500, 510, 100))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setItalic(True)
        self.cite_label.setFont(font)
        self.cite_label.setMouseTracking(False)
        self.cite_label.setReadOnly(True)
        self.cite_label.setObjectName("cite_label")
        self.btn_run.raise_()
        self.frame_2.raise_()
        self.frame_3.raise_()
        self.cite_label.raise_()
        self.copy_citation.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_run.setText(_translate("MainWindow", "Run\n(Please select directory)"))
        self.btn_dir.setText(_translate("MainWindow", "Select\n"
"Directory"))
        self.wav_folder.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt;\">[Please select a directory]</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Number of threads:"))
        self.wavs.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt;\">[No directory selected]</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Directory with wav files:"))
        self.label_3.setText(_translate("MainWindow", "Files to be processed:"))
        self.btn_min.setText(_translate("MainWindow", "_"))
        self.btn_exit.setText(_translate("MainWindow", "X"))
        self.label_4.setText(_translate("MainWindow", "Cough Detection Tool (v 1.0)"))
        self.copy_citation.setText(_translate("MainWindow", "Copy citation"))
        self.cite_label.setPlainText(_translate("MainWindow", "Did you find this tool useful? Please cite as:\n"
"Nikonas Simou; Nikolaos Stefanakis; Panagiotis Zervas, \"A Universal System for Cough Detection in Domestic Acoustic Environments\" in EUSIPCO 2020."))

    def minimize(self):
        self.showMinimized()

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
                self.btn_run.setText("RUN\n(Select a valid directory)")
                self.btn_run.setEnabled(False)
            self.wavs.setText(files)
            self.btn_dir.setText("Change\nDirectory")
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


    def copy_citation_(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(citation)
        # self.parent.update() # the text will stay there after the window is closed
        # self.copied_lbl_txt.set("(Copied!)")
        
    def run_main(self):
        global wav_folder, n_threads_to_use
        wav_folder = self.wav_folder.toPlainText()
        n_threads_to_use = int(self.num_of_threads.value())
        QtCore.QCoreApplication.instance().quit()


class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):
    #Stack over flow - draggable window
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dragPos = QtCore.QPoint()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowIcon(QtGui.QIcon('forth_disk.png'))
    def mousePressEvent(self, event):                                 # +
        self.dragPos = event.globalPos()
        
    def mouseMoveEvent(self, event):                                  # !!!
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()     



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    # MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    w = MyWin()
    w.show()
    app.exec()
    w.close()
    print("Starting execution. Please wait...")
    main(wav_folder, n_threads_to_use)
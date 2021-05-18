# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stacked.ui'
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
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 531, 611))
        self.stackedWidget.setObjectName("stackedWidget")
        self.SettingsPage = QtWidgets.QWidget()
        self.SettingsPage.setObjectName("SettingsPage")
        self.frame = QtWidgets.QFrame(self.SettingsPage)
        self.frame.setGeometry(QtCore.QRect(0, 0, 530, 610))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(221, 231, 199, 255), stop:1 rgba(238, 248, 214, 255));\n"
"border-radius: 10px\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 50, 490, 351))
        self.frame_2.setStyleSheet("background-color: rgb(227, 227, 227);border-radius:10px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.btn_dir = QtWidgets.QPushButton(self.frame_2)
        self.btn_dir.setGeometry(QtCore.QRect(90, 10, 151, 61))
        self.btn_dir.clicked.connect(self.select_dir)                
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_dir.setFont(font)
        self.btn_dir.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(60, 137, 109, 255), stop:1 rgba(60, 137, 109, 100));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.btn_dir.setObjectName("btn_dir")
        self.wav_folder = QtWidgets.QTextBrowser(self.frame_2)
        self.wav_folder.setGeometry(QtCore.QRect(26, 100, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.wav_folder.setFont(font)
        self.wav_folder.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wav_folder.setObjectName("wav_folder")
        self.label_1 = QtWidgets.QLabel(self.frame_2)
        self.label_1.setGeometry(QtCore.QRect(340, 70, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.wavs = QtWidgets.QTextBrowser(self.frame_2)
        self.wavs.setGeometry(QtCore.QRect(26, 180, 271, 141))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.wavs.setFont(font)
        self.wavs.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wavs.setObjectName("wavs")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(26, 160, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.num_of_threads = QtWidgets.QSpinBox(self.frame_2)
        self.num_of_threads.setGeometry(QtCore.QRect(340, 103, 91, 41))
        self.num_of_threads.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.num_of_threads.setMinimum(1)
        self.num_of_threads.setMaximum(20)
        self.num_of_threads.setObjectName("num_of_threads")
        self.frame_title = QtWidgets.QFrame(self.frame)
        self.frame_title.setGeometry(QtCore.QRect(0, 0, 531, 31))
        self.frame_title.setStyleSheet("background-color: rgba(1, 32, 15, 100)")
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.btn_min = QtWidgets.QPushButton(self.frame_title)
        self.btn_min.setGeometry(QtCore.QRect(470, 5, 20, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_min.setFont(font)
        self.btn_min.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color:rgb(240, 135, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(240, 135, 0, 150);\n"
"}")
        self.btn_min.setObjectName("btn_min")
        self.btn_min.clicked.connect(self.minimize)        
        self.btn_exit = QtWidgets.QPushButton(self.frame_title)
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
"background-color: rgb(235,0,0, 150);\n"
"}")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(self.on_closing)        
        self.title = QtWidgets.QLabel(self.frame_title)
        self.title.setGeometry(QtCore.QRect(11, -3, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAutoFillBackground(False)
        self.title.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.title.setObjectName("title")
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
        self.btn_run = QtWidgets.QPushButton(self.frame)
        self.btn_run.setGeometry(QtCore.QRect(160, 420, 221, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_run.setFont(font)
        self.btn_run.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(60, 137, 109, 255), stop:1 rgba(60, 137, 109, 100));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 10), stop:1 rgba(255, 255, 255, 10));\n"
"}\n"
"\n"
"")
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self.run_main)        
        self.copy_citation = QtWidgets.QPushButton(self.frame)
        self.copy_citation.setGeometry(QtCore.QRect(390, 570, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.copy_citation.setFont(font)
        self.copy_citation.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(60, 137, 109, 255), stop:1 rgba(60, 137, 109, 100));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.copy_citation.setObjectName("copy_citation")
        self.copy_citation.clicked.connect(self.copy_citation_)                
        self.stackedWidget.addWidget(self.SettingsPage)


        self.ResultsPage = QtWidgets.QWidget()
        self.ResultsPage.setObjectName("ResultsPage")
        self.frame_res = QtWidgets.QFrame(self.ResultsPage)
        self.frame_res.setGeometry(QtCore.QRect(0, 0, 530, 610))
        self.frame_res.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(221, 231, 199, 255), stop:1 rgba(238, 248, 214, 255));\n"
"border-radius: 10px\n"
"")
        self.frame_res.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_res.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_res.setObjectName("frame_res")
        self.frame_11 = QtWidgets.QFrame(self.frame_res)
        self.frame_11.setGeometry(QtCore.QRect(20, 80, 490, 361))
        self.frame_11.setStyleSheet("background-color: rgb(227, 227, 227);border-radius:10px;")
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.wav_folder_2 = QtWidgets.QTextBrowser(self.frame_11)
        self.wav_folder_2.setGeometry(QtCore.QRect(230, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.wav_folder_2.setFont(font)
        self.wav_folder_2.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.wav_folder_2.setObjectName("wav_folder_2")
        self.label_4 = QtWidgets.QLabel(self.frame_11)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.frame_11)
        self.label.setGeometry(QtCore.QRect(10, 60, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.results = QtWidgets.QPlainTextEdit(self.frame_11)
        self.results.setGeometry(QtCore.QRect(10, 90, 471, 251))
        self.results.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.results.setObjectName("results")
        fontRes = QtGui.QFont()
        fontRes.setPointSize(12)
        self.results.setFont(fontRes)
        self.filelist = QtWidgets.QComboBox(self.frame_11)
        self.filelist.setGeometry(QtCore.QRect(230, 60, 251, 22))
        self.filelist.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.filelist.setObjectName("filelist")
        self.filelist.activated.connect(self.change_results)
        self.btn_listen = QtWidgets.QPushButton(self.frame_11)
        self.btn_listen.setGeometry(QtCore.QRect(330, 280, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_listen.setFont(font)
        self.btn_listen.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(9, 144, 0, 255), stop:1 rgba(16, 255, 0, 255));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(16, 254, 0, 255), stop:1 rgba(171, 255, 166, 255))\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 10), stop:1 rgba(255, 255, 255, 10));\n"
"}\n"
"\n"
"")
        self.btn_listen.setObjectName("btn_listen")
        self.btn_listen.clicked.connect(self.listen_active_wav)
        self.frame_title_2 = QtWidgets.QFrame(self.frame_res)
        self.frame_title_2.setGeometry(QtCore.QRect(0, 0, 531, 31))
        self.frame_title_2.setStyleSheet("background-color: rgba(1, 32, 15, 100)")
        self.frame_title_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title_2.setObjectName("frame_title_2")
        self.btn_min_2 = QtWidgets.QPushButton(self.frame_title_2)
        self.btn_min_2.setGeometry(QtCore.QRect(470, 5, 20, 20))
        self.btn_min_2.clicked.connect(self.minimize)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_min_2.setFont(font)
        self.btn_min_2.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color:rgb(240, 135, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgba(240, 135, 0, 150);\n"
"}")
        self.btn_min_2.setObjectName("btn_min_2")
        self.btn_exit_2 = QtWidgets.QPushButton(self.frame_title_2)
        self.btn_exit_2.setGeometry(QtCore.QRect(500, 5, 20, 20))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_exit_2.setFont(font)
        self.btn_exit_2.setStyleSheet("QPushButton{ \n"
"border:none; \n"
"border-radius: 7px; \n"
"background-color: rgb(235, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(235,0,0, 150);\n"
"}")
        self.btn_exit_2.setObjectName("btn_exit_2")
        self.btn_exit_2.clicked.connect(self.on_closing)        
        self.title_2 = QtWidgets.QLabel(self.frame_title_2)
        self.title_2.setGeometry(QtCore.QRect(11, -3, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title_2.setFont(font)
        self.title_2.setAutoFillBackground(False)
        self.title_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.title_2.setObjectName("title_2")
        self.cite_label_2 = QtWidgets.QPlainTextEdit(self.frame_res)
        self.cite_label_2.setGeometry(QtCore.QRect(20, 500, 510, 100))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setItalic(True)
        self.cite_label_2.setFont(font)
        self.cite_label_2.setMouseTracking(False)
        self.cite_label_2.setReadOnly(True)
        self.cite_label_2.setObjectName("cite_label_2")
        self.copy_citation_2 = QtWidgets.QPushButton(self.frame_res)
        self.copy_citation_2.setGeometry(QtCore.QRect(390, 570, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.copy_citation_2.setFont(font)
        self.copy_citation_2.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(60, 137, 109, 255), stop:1 rgba(60, 137, 109, 100));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.copy_citation_2.setObjectName("copy_citation_2")
        self.copy_citation_2.clicked.connect(self.copy_citation_)        
        self.btn_xlsx = QtWidgets.QPushButton(self.frame_res)
        self.btn_xlsx.setGeometry(QtCore.QRect(300, 460, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_xlsx.setFont(font)
        self.btn_xlsx.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(60, 137, 109, 255), stop:1 rgba(60, 137, 109, 100));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 10), stop:1 rgba(255, 255, 255, 10));\n"
"}\n"
"\n"
"")
        self.btn_xlsx.setObjectName("btn_xlsx")
        self.btn_xlsx.clicked.connect(self.export_xlsx)
        self.btn_txt = QtWidgets.QPushButton(self.frame_res)
        self.btn_txt.setGeometry(QtCore.QRect(70, 460, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_txt.setFont(font)
        self.btn_txt.setStyleSheet("QPushButton{ \n"
"border:0.5px solid grey; \n"
"border-radius: 7px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(60, 137, 109, 255), stop:1 rgba(60, 137, 109, 100));\n"
"}\n"
"QPushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(172, 194, 170, 10), stop:1 rgba(255, 255, 255, 10));\n"
"}\n"
"\n"
"")
        self.btn_txt.setObjectName("btn_txt")
        self.btn_txt.clicked.connect(self.export_txt)
        self.title_res = QtWidgets.QLabel(self.frame_res)
        self.title_res.setGeometry(QtCore.QRect(30, 40, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title_res.setFont(font)
        self.title_res.setAutoFillBackground(False)
        self.title_res.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.title_res.setObjectName("title_res")
        self.stackedWidget.addWidget(self.ResultsPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_dir.setText(_translate("MainWindow", "Select\n"
"Directory"))
        self.wav_folder.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt;\">[Please select a directory]</span></p></body></html>"))
        self.label_1.setText(_translate("MainWindow", "Number of threads:"))
        self.wavs.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt;\">[No directory selected]</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Directory with wav files:"))
        self.label_3.setText(_translate("MainWindow", "Files to be processed:"))
        self.btn_min.setText(_translate("MainWindow", "_"))
        self.btn_exit.setText(_translate("MainWindow", "X"))
        self.title.setText(_translate("MainWindow", "Cough Detection Tool (v 1.0)"))
        self.cite_label.setPlainText(_translate("MainWindow", "Did you find this tool useful? Please cite as:\n"
"Nikonas Simou; Nikolaos Stefanakis; Panagiotis Zervas, \"A Universal System for Cough Detection in Domestic Acoustic Environments\" in EUSIPCO 2020."))
        self.btn_run.setText(_translate("MainWindow", "Run"))
        self.copy_citation.setText(_translate("MainWindow", "Copy citation"))
        self.wav_folder_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt;\">[Please select a directory]</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Directory with wav files scanned:"))
        self.label.setText(_translate("MainWindow", "Results per file:"))
        self.btn_listen.setText(_translate("MainWindow", "Click to listen\n"
"detections"))
        self.btn_min_2.setText(_translate("MainWindow", "_"))
        self.btn_exit_2.setText(_translate("MainWindow", "X"))
        self.title_2.setText(_translate("MainWindow", "Cough Detection Tool (v 1.0)"))
        self.cite_label_2.setPlainText(_translate("MainWindow", "Did you find this tool useful? Please cite as:\n"
"Nikonas Simou; Nikolaos Stefanakis; Panagiotis Zervas, \"A Universal System for Cough Detection in Domestic Acoustic Environments\" in EUSIPCO 2020."))
        self.copy_citation_2.setText(_translate("MainWindow", "Copy citation"))
        self.btn_xlsx.setText(_translate("MainWindow", "Save as .xlsx"))
        self.btn_txt.setText(_translate("MainWindow", "Save as .txt"))
        self.title_res.setText(_translate("MainWindow", "Results"))


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
                self.btn_run.setEnabled(True)
                self.btn_run.setText("Run")
            else:
                files = "No .wav files found in selected directory."
                self.btn_run.setText("Run\n(Select a valid directory)")
                self.btn_run.setEnabled(False)
            self.wavs.setText(files)
            self.btn_dir.setText("Change\nDirectory")
        #window.label_2.setText(file)


    def on_closing(self):
        import gc

        reply = QtWidgets.QMessageBox.question(self, 'Quit',
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

    def export_xlsx(self):
        if self.filelist.currentText()=="Select file":
            return
        import os
        fname = f'CoughResults/{self.filelist.currentText().replace(".wav", ".xlsx")}'
        i=1
        if os.path.exists(fname):
            fname = fname.replace(".xlsx", f"_{i}.xlsx")
            while os.path.exists(fname):
                i+=1
                fname = fname.replace(f"_{i-1}.xlsx", f"_{i}.xlsx")
        self.df.to_excel(fname)
        QtWidgets.QMessageBox.information(self, 'Save succesful!',
            f"File saved as\n{fname}", QtWidgets.QMessageBox.Ok)
        
    def export_txt(self):
        if self.filelist.currentText()=="Select file":
            return
        import os
        fname = f'CoughResults/{self.filelist.currentText().replace(".wav", ".txt")}'
        i=1
        if os.path.exists(fname):
            fname = fname.replace(".txt", f"_{i}.txt")
            while os.path.exists(fname):
                i+=1
                fname = fname.replace(f"_{i-1}.txt", f"_{i}.txt")
        with open(fname, 'w+') as file:
            file.write(self.df.to_string())
        QtWidgets.QMessageBox.information(self, 'Save succesful!',
            f"File saved as\n{fname}", QtWidgets.QMessageBox.Ok)


    def initialize_files(self):
        import glob, os, pandas as pd, numpy as np
        self.wav_folder_2.setText(wav_folder)
        cwd = os.getcwd().replace("\\", "/")
        found = glob.glob(f"{cwd}/CoughResults/*.txt")
        files = glob.glob(f"{wav_folder}/**/*.wav", recursive=True)
        self.df = pd.DataFrame()
        self.results.setPlainText("Please select a file to view cough segments detected.")
        self.results.setReadOnly(True)
        self.btn_listen.hide()
        self.btn_xlsx.hide()
        self.btn_txt.hide()
            
        if len(found)==0:
            self.filelist.addItem("-")
            self.results.setPlainText("No coughs found.")
            self.filelist.setEnabled(False)
        else:
            self.res_text = dict()
            self.extracted_wavs = dict()
            self.filelist.addItem("Select file")
            self.res_text["Select file"]="Please select a file to view cough segments detected."
            for f in found:
                cc = f.replace("\\", "/").split("/")[-1].split("_coughDetections.txt")[0]
                self.filelist.addItem(cc)
                self.df = pd.DataFrame(np.loadtxt(f)[:,1:], columns=["Time (s)", "Confidence"], index=np.loadtxt(f)[:,0].astype(int)) 
                self.res_text[cc] = self.df.to_string()
                self.extracted_wavs[cc] = f.replace(".txt", ".wav") #[fn for fn in files if cc in fn][0]

    def change_results(self):
        self.results.setPlainText(self.res_text[self.filelist.currentText()])
        check=self.filelist.currentText()!="Select file"
        if check:
            self.btn_listen.hide()
            self.btn_xlsx.hide()
            self.btn_txt.hide()
        else:
            self.btn_listen.show()
            self.btn_xlsx.show()
            self.btn_txt.show()
        # self.btn_listen.setEnabled(check)
        # self.btn_xlsx.setEnabled(check)
        # self.btn_txt.setEnabled(check)


    def listen_active_wav(self):
        if self.filelist.currentText()=="Select file":
            return
        from playsound import playsound
        playsound(self.extracted_wavs[self.filelist.currentText()])

    def run_main(self):
        global wav_folder, n_threads_to_use
        wav_folder = self.wav_folder.toPlainText()
        n_threads_to_use = int(self.num_of_threads.value())
        print("Starting execution. Please wait...")
        self.hide()
        main(wav_folder, n_threads_to_use)

        self.stackedWidget.setCurrentIndex(1)
        self.initialize_files()
        self.show()
        #QtCore.QCoreApplication.instance().quit()



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
    w = MyWin()
    w.show()
    sys.exit(app.exec())


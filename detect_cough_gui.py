import os
import sys
import tkinter as tk
import tkinter.ttk  as ttk
from tkinter import E, W, N, S

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



class CollapsiblePane(ttk.Frame):
# Implementation of Collapsible Pane container
# Adopted from 
# https://www.geeksforgeeks.org/collapsible-pane-in-tkinter-python/
    """
    -----USAGE-----
    collapsiblePane = CollapsiblePane(parent,
                        expanded_text =[string],
                        collapsed_text =[string])

    collapsiblePane.pack()
    button = Button(collapsiblePane.frame).pack()
    """

    def __init__(self, parent, expanded_text ="Collapse <<",
                            collapsed_text ="Expand >>"):

        ttk.Frame.__init__(self, parent)

        # These are the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means these are private to class
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text

        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        self.columnconfigure(1, weight = 1)

        # Tkinter variable storing integer value
        self._variable = tk.IntVar()

        # Checkbutton is created but will behave as Button
        # cause in style, Button is passed
        # main reason to do this is Button do not support
        # variable option but checkbutton do
        self._button = ttk.Checkbutton(self, variable = self._variable,
                            command = self._activate, style ="TButton")
        self._button.grid(row = 0, column = 0)

        # This wil create a seperator
        # A separator is a line, we can also set thickness
        self._separator = ttk.Separator(self, orient ="horizontal")
        self._separator.grid(row = 0, column = 1, sticky ="we")

        self.frame = ttk.LabelFrame(self)

        # This will call activate function of class
        self._activate()

    def _activate(self):
        if not self._variable.get():

            # As soon as button is pressed it removes this widget
            # but is not destroyed means can be displayed again
            self.frame.grid_forget()

            # This will change the text of the checkbutton
            self._button.configure(text = self._collapsed_text)

        elif self._variable.get():
            # increasing the frame area so new widgets
            # could reside in this container
            self.frame.grid(row = 1, column = 0, columnspan = 2)
            self._button.configure(text = self._expanded_text)

    def toggle(self):
        """Switches the label frame to the opposite state."""
        self._variable.set(not self._variable.get())
        self._activate()


cp = CollapsiblePane

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.wav_folder = tk.StringVar() 
        self.wav_folder.set("[No directory selected]")
        self.btn_lbl = tk.StringVar()
        self.dir_lbl_text = tk.StringVar()
        self.threadss = tk.IntVar()
        self.threadss.set(1)
        self.run_btn_text = tk.StringVar()
        self.run_btn_text.set("Run\n(Please select a directory)")
        self.fpos = {'del': 2, 'dir': 1, 'params': 4, 'ok': 8, 'cite': 10}
        self.parchoice = tk.IntVar()
        self.parchoice.set(2)
        


        self.btn_lbl.set("Click to select directory")
        dir_frame = ttk.LabelFrame(parent, text='Target directory containing audio data: ')
        dir_frame.grid(row=self.fpos['dir'], padx=10, pady=10, column=1, columnspan=3)        
        self.dir_lbl_text.set(f"Directory chosen: {self.wav_folder.get()}")
        dir_lbl = tk.Label(dir_frame, textvariable = self.dir_lbl_text, wraplength=300, justify='left')
        dir_lbl.grid(row=0, column=0, padx=(10), pady=10, rowspan=2)
        dir_btn = tk.Button(dir_frame, textvariable = self.btn_lbl, command=self.clicked_dir_button)
        dir_btn.grid(row=0, column=1, padx=(10), pady=10)
        self.dir_check_files_btn = tk.Button(dir_frame, text = "Check test files in folder", command=self.check_test_files, state=tk.DISABLED)
        self.dir_check_files_btn.grid(row=2, column=1, padx=(10), pady=10)

        pf = ttk.Labelframe(parent, text='Parameters')
        pf.grid(row=self.fpos['params'], column=0, columnspan=3,  padx=(20), pady=10, sticky=E+W+N+S)                
        params_row = {'threads':2}

        threads_lbl = tk.Label(pf, text = f"Maximum number of threads to use")
        threads_lbl.grid(row=params_row['threads'], column=0, padx=(10), pady=10)
        threads_f = tk.Frame(pf)
        threads_f.grid(row=params_row['threads'], column=1, pady=10, columnspan=2)
        threads_textbox = tk.Entry(pf, textvariable=self.threadss)
        threads_textbox.grid(row=params_row['threads'], column=1, padx=(10), pady=10)

        ok_frame = ttk.LabelFrame(parent, text = None)
        ok_frame.grid(row=self.fpos['ok'], column=2,  padx=10, pady=10, sticky=W+N+S)
        self.run_btn = tk.Button(ok_frame, textvariable = self.run_btn_text, 
        command=self.run_main, state=tk.DISABLED)
        self.run_btn.grid(padx=180, pady=10)#row=0, column=0, sticky = E+W+N+S)

        citepane = cp(parent, 'Hide citation 🔼', 'Show citation 🔽')
        cite_frame = citepane.frame

        citepane.grid(row=self.fpos['cite'], column=2, columnspan=1, padx=10, pady=10, sticky=E+W+N+S)
        
        cite_txt = 'If you find any of this library useful for your research please cite as:'
        cite_lbl = tk.Label(cite_frame, text = f"{cite_txt}\n\n{citation}", wraplength=350, justify='left')
        cite_lbl.grid(row=0, column=0, padx=(10), pady=10)
        copy_btn = tk.Button(cite_frame, text = "Copy to clipboard", command=self.copy_citation)
        copy_btn.grid(row=0, column=2, padx=(10), pady=10)
        self.copied_lbl_txt = tk.StringVar()
        copied_lbl = tk.Label(cite_frame, textvariable = self.copied_lbl_txt)
        copied_lbl.grid(row=4, column=2, padx=(10), pady=10)
        

    def parse_threads_radio(self):
        max_threadss = self.count_processors()
        choice_list = [1, max_threadss//4, max_threadss//2, max_threadss]
        # print(f"parchoice {self.parchoice.get()}, threadss = {self.threadss.get()}")
        threads_temp = choice_list[self.parchoice.get()]
        self.threadss.set(max([1, threads_temp]))
        # print(f"parchoice {self.parchoice.get()}, threadss = {self.threadss.get()}")


    def copy_citation(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(citation)
        self.parent.update() # the text will stay there after the window is closed
        self.copied_lbl_txt.set("(Copied!)")
        
    def run_main(self):
        global wav_folder, n_threads_to_use
        wav_folder = self.wav_folder.get()
        n_threads_to_use = self.threadss.get()
        self.parent.destroy()
        
    def clicked_dir_button(self, *args):
        import tkinter.filedialog
        newdir = tkinter.filedialog.askdirectory(parent=self.parent, 
        initialdir=os.getcwd(), 
        title='Please select the directory containing the target .wav files.')
        if newdir: 
        	self.wav_folder.set(newdir)
	        print(f"Directory chosen: {newdir}")
	        ch_txt = self.wav_folder.get()
	        # width = 50; begin = 8;
	        # if len(ch_txt)>width: ch_txt = f"{ch_txt[:begin]}...{ch_txt[-(width-begin-3):]}"
	        self.dir_lbl_text.set(f"Directory chosen: {ch_txt}")          
	        self.btn_lbl.set("Click to change directory")
	        self.run_btn_text.set("Run")
	        self.run_btn.config(state="normal")
	        self.dir_check_files_btn.config(state="normal")

    def on_closing():
        import tkinter.messagebox
        import gc
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            print('Thank you for using our tool!')
            gc.collect()
            exit()

    def check_test_files(self):      
        import glob
        	    # Toplevel object which will 
	    # be treated as a new window
        newWindow = tk.Toplevel(self.master)
        path = self.wav_folder.get()
        newWindow.title(f"Test files in {path}")
        files = [file.replace("\\", "/").split("/")[-1] for file in glob.glob(f"{path}/**/*.wav", recursive=True)]
        if len(files)<1: files = "[No .wav files in this folder or its subfolders]"
        else:
	        files = '\n'.join(files)
        text = tk.Text(newWindow)
        text.pack()
        text.insert(tk.END,files)
        text.configure(state='disabled')	  	    


if __name__ == "__main__":
    global wav_folder, n_threads_to_use
    root = tk.Tk()
    root.title("Cough detection (GUI version)")
    MainApplication(root)
    root.protocol("WM_DELETE_WINDOW", MainApplication.on_closing)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()
    print("Starting execution. Please wait...")
    main(wav_folder, n_threads_to_use)
    

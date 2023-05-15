import sys
import threading
import PySimpleGUI as sg
from subprocess import call
import time
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import os
import dropbox
from dropbox.files import WriteMode

event = "Record Locally"

def auto_record(event, duration):
    global recording
    fs = 44100
    file_number = 1
    
    while event != 'Quit' and recording:
        now = datetime.now()
        date_string = now.strftime("%m-%d-%Y")
        time_string = now.strftime("%H:%M:%S")
        file_name = "Beehive" + str(file_number) + "-" + date_string + "-" + time_string[0:5]
        print("          ")
        
        print(f"-> Recording File [{file_number}]...")
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write(file_name, fs, myrecording)

        print(f"File saved as {file_name}")
        print(f"{file_number} file(s) recorded in this session so far. Length: {duration} seconds.\n")
        
        file_number += 1

autoRun = False

while True:
        
    if not autoRun:
        print("Launching BeePro...")
        autoRun = True
        duration = 900
        print("Duration set to:", duration, "seconds")
        recording = True
        threading.Thread(target=auto_record, args=(event, duration), daemon=True).start()
            

class Unbuffered(object):
    def __init__(self, window):
        self.window = window

    def write(self, data):
        self.window.write_event_value("OUT", data)

    def writelines(self, datas):
        self.window.write_event_value("OUT", ''.join(datas))


sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
window.close()

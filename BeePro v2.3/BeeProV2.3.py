 # imported libraries
import sys
import threading
import PySimpleGUI as sg
from subprocess import call
import time
import os
from datetime import datetime, date, timezone 
import sounddevice as sd
from scipy.io.wavfile import write
import subprocess

def local():
    print("-> Saving on local storage...")
    now = datetime.now()  # this variable gets the date and time

    deadline = date(2099, 10, 30)  # the date of the deadline (you can set this to whatever date you want using the
    # format year, month, day)
    current_date = now.date()  # this will be the current date
    file_number = 1  # this will be the variable to update in every loop after you create a file to save the files
    # using incremental numbers

    # these 2 variables are just to format the date and time in a readable way
    # mm/dd/YY
    date_string = now.strftime("%m-%d-%Y")
    # H:M:S
    time_string = now.strftime("%H:%M:%S")

    fs = 44100
    file_name = "Beehive" + str(file_number) + "-" + date_string + "-" + time_string[
                                                                         0:5]  # file + file number + date + hour
    #duration = newTime  # seconds of length for each WAV file
    print('-> Snipping every, ', duration, 'seconds...')

    while event != 'Quit':
        print("-> Recording File [", file_number, "]...")
        # save wav file
        file_name = "Beehive" + str(file_number) + "-" + date_string + "-" + time_string[
                                                                             0:5]  # file + file number + date + hour
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        write(file_name, fs, myrecording)  # Save as WAV file
        now = datetime.now()
        date_string = now.strftime("%m-%d-%Y")
        time_string = now.strftime("%H:%M:%S")
        file_name = "Beehive" + str(file_number + file_number) + "-" + date_string + "-" + time_string[
                                                                                           0:5]  # file + file number + date + hour
        file_number += 1  # increase file number for the next file
                
        print("File saved as " + file_name)
            
        print(file_number - 1, "file(s) recorded in this session so far. Length: ", duration, "seconds.")
        print("")
        # print(time_string.split(":")[1])


def cloud():
    print("-> Saving on cloud storage...")
    now = datetime.now()  # this variable gets the date and time

    deadline = date(2099, 10, 30)  # the date of the deadline (you can set this to whatever date you want using the
    # format year, month, day)
    current_date = now.date()  # this will be the current date
    file_number = 1  # this will be the variable to update in every loop after you create a file to save the files
    # using incremental numbers

    # these 2 variables are just to format the date and time in a readable way
    # mm/dd/YY
    date_string = now.strftime("%m-%d-%Y")
    # H:M:S
    time_string = now.strftime("%H:%M:%S")

    fs = 44100
    file_name = "Beehive" + str(file_number) + "-" + date_string + "-" + time_string[
                                                                         0:5]  # file + file number + date + hour
    #duration = newTime  # seconds of length for each WAV file
    print('-> Snipping every, ', duration, 'seconds...')

    while event != 'Quit':
        print("-> Recording File [", file_number, "]...")
        # save wav file
        file_name = "Beehive" + str(file_number) + "-" + date_string + "-" + time_string[
                                                                             0:5]  # file + file number + date + hour
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        write(file_name, fs, myrecording)  # Save as WAV file
        now = datetime.now()
        date_string = now.strftime("%m-%d-%Y")
        time_string = now.strftime("%H:%M:%S")
        file_name = "Beehive" + str(file_number + file_number) + "-" + date_string + "-" + time_string[
                                                                                           0:5]  # file + file number + date + hour
        file_number += 1  # increase file number for the next file
        print("File saved as " + file_name)
        print(file_number - 1, "file(s) recorded in this session so far. Length: ", duration, "seconds.")
        rc = call("./googleUpload", shell=True)
        # print(time_string.split(":")[1])


def edgeImpulse():
    print("-> [HOLD] Attempting to Establish Cloud Connection...\n")
    print("-> [SUCCESS] Edge-Impulse Connected Successfully. Refer to Terminal.")
    time.sleep(3)

    rc = call("./cloudEI", shell=True)

    print("-> [ERROR] Command Line Opened.")
    time.sleep(2)
    print("-> Refer to Terminal for Error Message.\n")
    print("-> [CONNECTION FAILED. Relaunch.]")

class Unbuffered(object):
    def __init__(self, window):
        self.window = window

    def write(self, data):
        self.window.write_event_value("OUT", data)

    def writelines(self, datas):
        self.window.write_event_value("OUT", ''.join(datas))


# --------------------------- FULL GUI LAYOUT ---------------------------
sg.theme('DarkBlue2')

frame_layout = [[sg.Multiline("", size=(80, 20), autoscroll=True, key='-OUTPUT-', background_color="#111111",
                              text_color="#FFFFFF")]]
layout = [
    [sg.Frame("Output Console", frame_layout)],
    [sg.Text('Duration (in seconds)', size=(18,1), pad=(0,0)), sg.InputText(key='newTime', size=(6,1)), sg.Button('Set')],
    [sg.Push(), sg.Button("R/U to Google Drive"), sg.Button("Run Locally"), sg.Button("Connect EdgeImpulse"), sg.Button('Quit')]]

window = sg.Window("BeePro - Version 2.30", layout, finalize=True)
old_stdout, old_stderr = sys.stdout, sys.stderr
sys.stdout = Unbuffered(window)
sys.stderr = Unbuffered(window)
printing = False

print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print(" |           __          . '  '  .   ")
print(" |        _/__)         .     .              .    Welcome to BeePro.")
print(" |     (8|)_}}--  .        .               .       Linux Version 2.30  ")
print(" |        `\__)     ' .  .  '  '  .   .  '    ")
print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

print("-> NOTE: Please set a duration time BEFORE running.\n")

# --------------------------- EVENT LOOP ---------------------------
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Run Locally':
        time.sleep(1)
        threading.Thread(target=local, daemon=True).start()
    elif event == 'Quit':
        print("Quitting Program...")
        rc = call("./closeTerm", shell=True)
        break
    elif event == 'Connect EdgeImpulse':
        threading.Thread(target=edgeImpulse, daemon=True).start()
    elif event == 'Set':
        duration = int(values['newTime'])
        print("--> Duration between each recording has been changed to:", duration, "seconds" )
    elif event == "OUT":
        window['-OUTPUT-'].update(values["OUT"], append=True)
    elif event == 'R/U to Google Drive':
        threading.Thread(target=cloud, daemon=True).start()
        print("")
        
sys.stdout, sys.stderr = old_stdout, old_stderr
window.close()

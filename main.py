from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from ttkthemes import ThemedTk

from scipy.io import wavfile
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import dsp

sampleRate, samples = wavfile.read("test.wav")
dataIsolated, dataStart, dataEnd = dsp.signalIsolate(samples, sampleRate, 500)
dataZeros, dataPeaks, dataTimings = dsp.findTimings(dataIsolated)
for i, data in enumerate(dataTimings):
    dataTimings[i] = data*1000
dataTimingsX = []
for i in range(1, len(dataPeaks)):
    dataTimingsX.append(dataPeaks[i])
lower, higher, average, bits = dsp.boundsDecode(dataTimings, 6, 1.3)

def selectFile():
    global sampleRate, samples
    filetypes = (('wav files', '*.wav'), ('All files', '*.*'))

    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    print(filename)

    sampleRate, samples = wavfile.read(filename)

def decodeSelected():
    global dataIsolated, dataStart, dataEnd, dataZeros, dataPeaks, dataTimings, dataTimingsX, lower, higher, average, bits
    dataIsolated, dataStart, dataEnd = dsp.signalIsolate(samples, sampleRate, 3000)
    dataZeros, dataPeaks, dataTimings = dsp.findTimings(dataIsolated)
    for i, data in enumerate(dataTimings):
        dataTimings[i] = data*1000
    dataTimingsX = []
    for i in range(1, len(dataPeaks)):
        dataTimingsX.append(dataPeaks[i])
    lower, higher, average, bits = dsp.boundsDecode(dataTimings, 10, 2)
    if trackOneSelected.get() == 1:
        rawTrackOne.delete(1.0,END)
        rawTrackOne.insert(END, bits)
    if trackTwoSelected.get() == 1:
        rawTrackTwo.delete(1.0,END)
        rawTrackTwo.insert(END, bits)
    if trackThreeSelected.get() == 1:
        rawTrackThree.delete(1.0,END)
        rawTrackThree.insert(END, bits)
    #cardValue1.config(text = int(lowerbits[68:80], 2)/100)
    #cardValue2.config(text = int(upperbits[68:80], 2)/100)

def showDisplay():
    plt.plot(dataIsolated, linestyle = "solid", color = "purple", zorder = 0)
    plt.scatter(dataZeros, dataIsolated[dataZeros], zorder = 1)
    plt.scatter(dataPeaks, dataIsolated[dataPeaks], zorder = 2)
    plt.plot(dataTimingsX, dataTimings, linestyle = "solid", color = "blue", zorder = 3)
    plt.plot(dataTimingsX, lower, linestyle = "solid", color = "red", zorder = 4)
    plt.plot(dataTimingsX, higher, linestyle = "solid", color = "green", zorder = 5)
    plt.plot(dataTimingsX, average, linestyle = "solid", color = "orange", zorder = 6)
    plt.show()

def hideDisplay():
    plt.close("all")

#ROOT CREATE
root = ThemedTk(theme="", gif_override = True)
root.title("Magtility")
trackOneSelected = IntVar()
trackTwoSelected = IntVar()
trackThreeSelected = IntVar()
#ROOT WEIGHTS
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

#CREATE FRAMES
logoFrame = ttk.LabelFrame(root)
wavFrame = ttk.LabelFrame(root, text = "Load Wav")
displayFrame = ttk.LabelFrame(root, text = "Data Display")
binaryFrame = ttk.LabelFrame(root, text = "Raw Binary")
#PLACE FRAMES
logoFrame.grid(row = 0, column = 0, sticky = 'nsew')
wavFrame.grid(row = 1, column = 0, sticky = 'nsew')
displayFrame.grid(row = 2, column = 0, sticky = 'nsew')
binaryFrame.grid(row = 0, column = 1, rowspan = 3, sticky = 'nsew')
#FRAME WEIGHTS
wavFrame.grid_columnconfigure(0, weight=1)
wavFrame.grid_columnconfigure(1, weight=1)
wavFrame.grid_columnconfigure(2, weight=1)
wavFrame.grid_rowconfigure(0, weight=1)
wavFrame.grid_rowconfigure(1, weight=1)
wavFrame.grid_rowconfigure(2, weight=1)

displayFrame.grid_columnconfigure(0, weight=1)
displayFrame.grid_rowconfigure(0, weight=1)
displayFrame.grid_rowconfigure(1, weight=1)

#LOGO CREATE AND PLACE
cardLogo = PhotoImage(file = "logo.png")
ttk.Label(logoFrame, image = cardLogo).pack()

#WAV WIDGETS CREATE
selectFile = ttk.Button(wavFrame, text = "Select File", command = selectFile)
trackOneSelect = ttk.Checkbutton(wavFrame, text='Track 1',variable=trackOneSelected , onvalue=1, offvalue=0)
trackTwoSelect = ttk.Checkbutton(wavFrame, text='Track 2',variable=trackTwoSelected , onvalue=1, offvalue=0)
trackThreeSelect = ttk.Checkbutton(wavFrame, text='Track 3',variable=trackThreeSelected , onvalue=1, offvalue=0)
loadFile = ttk.Button(wavFrame, text = "Load File", command = decodeSelected)
#WAV WIDGETS PLACE
selectFile.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew')
trackOneSelect.grid(row = 1, column = 0, sticky = 'nsew')
trackTwoSelect.grid(row = 1, column = 1, sticky = 'nsew')
trackThreeSelect.grid(row = 1, column = 2, sticky = 'nsew')
loadFile.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew')

#DISPLAY WIDGETS CREATE
displayData = ttk.Button(displayFrame, text = "Display Data", command = showDisplay)
hideData = ttk.Button(displayFrame, text = "Hide Data", command = hideDisplay)
#DISPLAY WIDGETS PLACE
displayData.grid(row = 0, column = 0, sticky = 'nsew')
hideData.grid(row = 1, column = 0, sticky = 'nsew')

#RAW BINARY WIDGETS CREATE
rawTrackOne = Text(binaryFrame, height = 4)
rawTrackTwo = Text(binaryFrame, height = 4)
rawTrackThree = Text(binaryFrame, height = 4)
ttk.Label(binaryFrame, text = "Track One:").grid(row = 0, column = 0, sticky = 'nsew')
ttk.Label(binaryFrame, text = "Track Two:").grid(row = 1, column = 0, sticky = 'nsew')
ttk.Label(binaryFrame, text = "Track Three:").grid(row = 2, column = 0, sticky = 'nsew')
#RAW BINARY WIDGETS PLACE
rawTrackOne.grid(row = 0, column = 1)
rawTrackTwo.grid(row = 1, column = 1)
rawTrackThree.grid(row = 2, column = 1)

root.mainloop()
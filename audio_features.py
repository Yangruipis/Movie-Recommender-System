import numpy as np
import pandas as pd
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import os


def preProcess(fileName):

    # Extracting wav file data

    [Fs, x] = audioBasicIO.readAudioFile(fileName)

    # If double channel data then take mean

    if len(x.shape) > 1 and x.shape[1] == 2:
        x = np.mean(x, axis=1, keepdims=True)
    else:
        x = x.reshape(x.shape[0], 1)

    # Extract the raw chromagram data, expected dimention is [ m,  ] not [ m, 1 ]

    (F, f_names) = audioFeatureExtraction.stFeatureExtraction(x[:, 0],
            Fs, 0.050 * Fs, 0.025 * Fs)

    return (f_names, F)


def getChromagram(audioData):

    # chronograph_1

    temp_data = audioData[21].reshape(1, audioData[21].shape[0])
    chronograph = temp_data

    # looping through the next 11 stacking them vertically

    for i in range(22, 33):
        temp_data = audioData[i].reshape(1, audioData[i].shape[0])
        chronograph = np.vstack([chronograph, temp_data])

    return chronograph


def getNoteFrequency(chromagram):

    # Total number of time frames in the current sample

    numberOfWindows = chromagram.shape[1]

    # Taking the note with the highest amplitude

    freqVal = chromagram.argmax(axis=0)

    # Converting the freqVal vs time to freq count

    (histogram, bin) = np.histogram(freqVal, bins=12)

    # Normalizing the distribution by the number of time frames

    normalized_hist = histogram.reshape(1, 12).astype(float) \
        / numberOfWindows

    return normalized_hist


def plotHeatmap(chromagram, smallSample=True):

    notesLabels = [
        'G#',
        'G',
        'F#',
        'F',
        'E',
        'D#',
        'D',
        'C#',
        'C',
        'B',
        'A#',
        'A',
        ]

    (fig, axis) = plt.subplots()

    if smallSample:
        im = axis.imshow(chromagram[:, 0:25], cmap='YlGn')
    else:
        im = axis.imshow(chromagram)

    cbar = axis.figure.colorbar(im, ax=axis, cmap='YlGn')
    cbar.ax.set_ylabel('Amplitude', rotation=-90, va='bottom')

    axis.set_yticks(np.arange(len(notesLabels)))
    axis.set_yticklabels(notesLabels)

    axis.set_title('chromagram')

    fig.tight_layout()
    _ = plt.show()


def noteFrequencyPlot(noteFrequency, smallSample=True):

    (fig, axis) = plt.subplots(1, 1, sharey=True)

    axis.plot(np.arange(1, 13), noteFrequency[0, :])

    _ = plt.show()


def plotOneFile(filename):
    (feature_name, features) = preProcess(filename)

    chromagram = getChromagram(features)
    print(chromagram)
    plotHeatmap(chromagram)


def getDataset(filePath):
    fileList = []
    X = pd.DataFrame()

    columns = [
        'G#',
        'G',
        'F#',
        'F',
        'E',
        'D#',
        'D',
        'C#',
        'C',
        'B',
        'A#',
        'A',
        ]

    for (root, dirs, filenames) in os.walk(filePath):
        for file in filenames:
            print(file)
            try:
                (feature_name, features) = preProcess(filePath + file)
                chromagram = getChromagram(features)
                noteFrequency = getNoteFrequency(chromagram)
                x_new = pd.Series(noteFrequency[0, :])
                X = pd.concat([X, x_new], axis=1)
                fileList.append(file)
            except:
                print("error")

    data = X.T.copy()
    data.columns = columns
    data.index = [i for i in range(0, data.shape[0])]

    return data


data = getDataset('sound/')
data.to_csv('data/sound_test.csv', index=False)

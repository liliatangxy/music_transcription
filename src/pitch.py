import librosa
import numpy as np

import note
import peakprocessing

'''
Functions to process pitches
'''

# frequency range on piano
min_freq = 27
max_freq = 4308

max_len = 97
filter_start = 261 # middle C
threshold = 34  # TODO: determine base threshold empirically
#threshold = 35
#threshold  = 10
note_index = {'C':0, 'C#':1, 'D':2, 'D#':3,
              'E':4, 'F':5, 'F#':6, 'G':7,
              'G#':8, 'A':9, 'A#':10, 'B':11}
def shift_pitch(y, sr):
    '''
    Returns pitch shifted without percussion
    '''
    y_harmonic = librosa.effects.harmonic(y)
    tuning = librosa.estimate_tuning(y=y_harmonic, sr=sr)
    y_tune = librosa.effects.pitch_shift(y, sr, -tuning)
    return y_tune

def _hps(d):
    # Hanning window
    #hanning = np.hanning(max_freq)
    #for i in range(0, max_freq):
    #    d[i] *= hanning[i]

    # first-order low-pass filter
    for i in range(filter_start+1, d.shape[0]):
        factor = i/filter_start
        d[i] /= factor
    return d

def detect_pitches(y, sr):
    '''
    Returns a list of notes
    Detected through STFT and HPS
    '''
    y_harmonic = librosa.effects.harmonic(y)
    onset_frame = librosa.onset.onset_detect(y_harmonic, sr=sr)
    d = librosa.stft(y_harmonic, sr=sr)

    d = _hps(d)
    d = librosa.logamplitude(d**2)

    note_list = []

    #for i in range(min_freq, max_freq):
    #    d[i] = peakprocessing.smooth(d[i])
    clustered = __cluster_notes(d)
    return d
   
def __cluster_notes(d, low_freq=min_freq, high_freq=max_freq):
    '''
    Groups frequencies representing the same note
    By default ignores notes not within piano frequency range
    '''
    clustered_notes = np.zeros((max_len, d.shape[1]))
    for i in range(low_freq, high_freq):
        n = librosa.core.hz_to_note(i)
        p = n[0][:len(n[0])-1]
        octave = n[0][len(n[0])-1]
        index = 12*int(octave) + note_index[p]
        for j in range(0, d.shape[1]):
            if d[i][j] >= threshold:
                clustered_notes[index][j] = max(d[i][j], clustered_notes[index][j])
                #if clustered_notes[index][j] > threshold:
                    #print(index_note[index-12*int(index/12)], int(index/12), j, clustered_notes[index][j])
    return clustered_notes

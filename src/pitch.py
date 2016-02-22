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
index_note = {0:'C', 1:'C#', 2:'D', 3:'E-',
              4:'E', 5:'F', 6:'F#', 7:'G',
              8:'A-', 9:'A', 10:'B-', 11:'B'}
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

def _first_peaks(d_clustered):
    print(d_clustered.shape[0], d_clustered.shape[1])
    for i in range(0, d_clustered.shape[1]):
        harmonics_idx = __detect_harmonics(d_clustered[:,i])
        for h in harmonics_idx:
            d_clustered[h][i] = 0
    return d_clustered

def __detect_harmonics(pitches_clustered):
    '''
    Returns indeces of potential harmonics
    '''
    # TODO values are already notes
    potential_f0s = []
    potential_harmonics = []
    for j in range(0, len(pitches_clustered)):
        potential_f0 = pitches_clustered[0]
        potential_f0s.append(potential_f0)
        for i in range(j+1, len(pitches_clustered)):
            f = pitches_clustered[i]
            if round((f-potential_f0) / 12) - (f-potential_f0) / 12 == 0:
                potential_harmonics.append(i)
    return potential_harmonics

def detect_pitches(y, sr):
    '''
    Returns a list of notes
    Detected through STFT and HPS
    '''
    y_harmonic = librosa.effects.harmonic(y)
    #onset_frame = librosa.onset.onset_detect(y_harmonic, sr=sr)
    d = librosa.stft(y_harmonic, sr)

    d = _hps(d)
    d = librosa.logamplitude(d**2)

    note_list = []

    #for i in range(min_freq, max_freq):
    #    d[i] = peakprocessing.smooth(d[i])
    clustered = _first_peaks(__cluster_notes(d))
    return stft_to_notes(clustered)

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

def stft_to_notes(d):
    '''
    Uses result from stft after clustering frequencies representing the same note to create a list of Notes
    '''
    note_list = []
    for i in range(0, max_len):
        peaks, valleys = peakprocessing.find_extrema(d[i])
        for p in peaks:
            while len(valleys) != 0 and valleys[0] < p:
                valleys.remove(valleys[0])
            if len(valleys) != 0:
                print(index_note[i-12*int(i/12)], int(i/12), p, valleys[0], d[i][p], d[i][valleys[0]])
                for j in range(p, valleys[0]):
                    print(d[i][j])
                #duration = librosa.core.frames_to_time(frames=valleys[0]-p+1, sr=sr)
                duration = valleys[0]-p+1
            else:
                #duration = librosa.core.frames_to_time(frames=1, sr=sr)
                duration = 1
            #start = librosa.core.frames_to_time(frames=p, sr=sr)
            start = p
            new_note = note.Note(name=index_note[i-12*int(i/12)], octave=int(i/12), start=start, duration=duration)
            note_list.append(new_note)
    note_list.sort(key=lambda n: n.start)

    for i in note_list:
        print(i.name, i.octave, i.start, i.duration)
    return note_list

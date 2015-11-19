import librosa
import numpy as np

import note

'''
Functions to process pitches
'''

def shift_pitch(y, sr):
    '''
    Returns pitch shifted without percussion
    '''
    y_harmonic = librosa.effects.harmonic(y)
    tuning = librosa.estimate_tuning(y=y_harmonic, sr=sr)
    y_tune = librosa.effects.pitch_shift(y, sr, -tuning)
    return y_tune

def determine_pitches(y, sr):
    '''
    Determines pitches
    '''
    y_harmonic = librosa.effects.harmonic(y)
    d = librosa.logamplitude(librosa.stft(y_harmonic, sr)**2, ref_power=np.max)
    
    note_list = [] # stores note with pitch, start time, duration in time

    current_n = [[0,0]] * d.shape[0] # current [start,duration] of note in loop
    threshold = -8
    for i in range(0, d.shape[1]):
        for j in range(0, d.shape[0]):
            if d[j][i] >= threshold:
                current_n[j][1] += 1
                if i == d.shape[0] - 1:
                    start = librosa.core.frames_to_time(current_n[j][0])
                    duration = librosa.core.frames_to_time(current_n[j][1])
                    new_note = note.Note(j, start, duration)
                    note_list.append(new_note)
            elif current_n[j][1] != 0:
                start = librosa.core.frames_to_time(current_n[j][0])
                duration = librosa.core.frames_to_time(current_n[j][1])
                new_note = Note(j, start, duration)
                note_list.append(new_note)
                current_n[j][0] = 0
                current_n[j][1] = 0
    # TODO may need to implement more efficient sort since notes are likely only unsorted within one measure
    note_list.sort(key=lambda n: n.start)
    return note_list

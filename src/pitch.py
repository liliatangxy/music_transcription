import librosa
import numpy as np

from note import Note

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
    chromagram = librosa.feature.chroma_stft(y_harmonic, sr)
    # TODO store notes in order they appear, not order they end
    note_list = [] # stores note with pitch, start time, duration in time
    current_d = [0] * 12 # current duration of note in loop
    threshold = 0.9
    for i in range(0, chromagram[0].size):
        for j in range(0, 12):
            if chromagram[j][i] >= threshold:
                current_d[j] += 1
                if i == chromagram[0].size - 1:
                    start = librosa.core.frames_to_time(i)
                    duration = librosa.core.frames_to_time(current_d[j])
                    new_note = Note(j, start, duration)
                    note_list.append(new_note)
            elif current_d[j] != 0:
                # TODO store pitch with octave
                start = librosa.core.frames_to_time(i)
                duration = librosa.core.frames_to_time(current_d[j])
                new_note = Note(j, start, duration)
                note_list.append(new_note)
                current_d[j] = 0
    return note_list

from music21 import *
import librosa

import peakprocessing
import pitch

max_len = 97
index_note = {0:'C', 1:'C#', 2:'D', 3:'E-',
              4:'E', 5:'F', 6:'F#', 7:'G',
              8:'A-', 9:'A', 10:'B-', 11:'B'}

class Note:
    def __init__(self, name, octave, start, duration):
        self.name = name 
        self.octave = octave
        self.start = start
        self.duration = duration

def stft_to_notes(d):
    '''
    Uses result from stft after clustering frequencies representing the same note to create a list of Notes
    '''
    for i in range(0, max_len):
        peaks, valleys = peakprocessing.find_extrema(clustered[i])
        for p in peaks:
            while len(valleys) != 0 and valleys[0] < p:
                valleys.remove(valleys[0])
            if len(valleys) != 0:
                print(index_note[i-12*int(i/12)], int(i/12), p, valleys[0], clustered[i][p], clustered[i][valleys[0]])
                for j in range(p, valleys[0]):
                    print(clustered[i][j])
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

def notes_to_stream(note_list):
    '''
    Uses list of Notes to convert to music21 stream
    '''
    # TODO separate hands and voices
    s = stream.Stream()
    c = []
    for i in range(0, len(note_list)):
        n = note_list[i]
        if and i != len(note_list-1):
            c.append(note.Note(n.name+str(n.octave), quarterLength=i.duration))
            if note_list[i+1].start != n.start:
                if len(c) > 1:
                    s.append(chord.Chord(c))
                else:
                    s.append(c)
    s.show()

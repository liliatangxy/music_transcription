import librosa

class Note:
    def __init__(self, name, octave, start, duration):
        self.name = name 
        self.octave = octave
        self.start = start
        self.duration = duration

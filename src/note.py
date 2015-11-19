import librosa

class Note:
    def __init__(self, pitch, start, duration):
        self.pitch = pitch
        self.start = start
        self.duration = duration

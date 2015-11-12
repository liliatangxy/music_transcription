import librosa

def load_sound(filename):
    y, sr = librosa.load(filename)
    return y, sr 

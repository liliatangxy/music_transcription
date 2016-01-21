import librosa

def determine_tempo(y, sr):
    onset_env = librosa.onset.onset_strength(y, sr)
    return librosa.beat.estimate_tempo(onset_env, sr=sr)

def determine_time_sig(y, sr):
    onset_env = librosa.onset.onset_strength(y, sr)
    tempogram = librosa.feature.tempogram(y, sr, onset_env)

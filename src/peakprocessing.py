import numpy as np
import math

def smooth(y_axis, m=3):
    '''
    Applies unweighted sliding-average smooth
    '''
    total = 0
    for k in range(0, m):
        total += y_axis[k]
    dif = y_axis[m/2]
    y_axis[m/2] = total/m
    dif -= total/m
    total -= dif
    for k in range(m, len(y_axis)):
        total += y_axis[k] - y_axis[k-m]
        dif = y_axis[k-m/2]
        y_axis[k-m/2] = total/m
        dif -= y_axis[k-m/2]
        total -= dif
    return y_axis

def kurtosis(y_axis, min_left, min_right):
    '''
    Calculates kurtosis of a peak given the indeces of its range
    Range likely consists of the local minima about the local maximum
    '''
    # TODO may need to write out std since mean is calculated twice
    variance = np.var(y_axis[min_left:min_right+1])
 
    # Calculate moment
    mean = 0
    length = min_right+1 - min_left
    for _, y in enumerate(y_axis[min_left:min_right+1]):
        mean += y
    mean /= length

    moment = 0
    for _, y in enumerate(y_axis[min_left:min_right+1]):
        moment += math.pow(y - mean, 4)
    moment /= length

    return moment / math.pow(variance, 2)


def find_extrema(y_axis, window=1):
    '''
    Finds local maxima and minima that are greater than all values within a window
    Returns indeces of maxima, minima
    '''
    peaks = []
    valleys = []
    length = len(y_axis)
    if y_axis[0] == y_axis[:window+1].max():
        peaks.append(0)
    elif y_axis[0] == y_axis[:window+1].min():
        valleys.append(0)
    for i in range(window, length-window):
        dif_before = y_axis[i]-y_axis[i-window]
        dif_after = y_axis[i+window]-y_axis[i]
        if dif_before*dif_after < 0:
            if dif_before > 0:
                peaks.append(i)
            if dif_before < 0:
                valleys.append(i)
    if y_axis[length-1] == y_axis[-window-1:].max():
        peaks.append(length-1)
    elif y_axis[length-1] == y_axis[-window-1:].min():
        valleys.append(length-1)
    return peaks, valleys

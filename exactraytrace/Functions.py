import numpy as np

#This arange function is designed to be more precise with floating point numbers
def safe_arange(start, stop, step, dec):
    round_start = round(start, dec)
    round_stop = round(stop, dec)
    int_start = round(round_start/step)
    int_stop = round(round_stop/step)

    return step * np.arange(int_start, int_stop+1)

def circle_eq(vals, center, radius):
    return (vals[0]-center[0])**2 + (vals[1]-center[1])**2 - radius**2
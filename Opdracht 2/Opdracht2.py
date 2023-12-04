from Libs.mbrtc import *
from scipy.signal import tf2ss


tel =     [1]
noem = [1, 1, 0]



H = tf2ss(tel,noem)

print(H)
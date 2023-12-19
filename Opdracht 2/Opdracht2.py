from Libs.mbrtc import *
from scipy.signal import *
import matplotlib.pyplot as plt

tel =     [1]
noem = [1, 1, 0]

H = tf2ss(tel,noem)

S = StateSpace(H[0],H[1],H[2],H[3])

print(S)
maxSeconds = 5

hstep = 6


print("System:")
print(f'A: {H[0]}')
print(f'B: {H[1]}')
print(f'C: {H[2]}')
print(f'D: {H[3]}')

print("Pole: \n [-1, 0]")

impulseResponse = impulse(H )
stepResponse = step(H)


plt.plot(impulseResponse[0],impulseResponse[1],"r--",stepResponse[0],stepResponse[1])
plt.xlabel('Step (h)')
plt.ylabel('Value (x)')
plt.legend(["Impulse", "Step"])
plt.show()


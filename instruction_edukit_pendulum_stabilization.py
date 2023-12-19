import numpy as np
from matplotlib import pyplot as plt
import scipy.signal as sgnl
from scipy.optimize import minimize
from mbrtc import *

# Step 1 - 5 and 12 and following are optional, but necessary if you want to implement the
# controller on your edukit setup and want the best performance. These steps may also be
# repeated, when you switch to another edukit setup.

# Step 1) In the edukit controller, without any controller on (so open-loop),
# Make a step-like control signal by entering (note s is an alias of supervisory)
# mp s['control_add'] = True
# Step 2) Then turn on the data recording by
# mp s['record'] = True
# Step 3) Wait at least two seconds and then you may turn off the step signal by
# mp s['control_add'] = False
# Step 4) print the recorded values on screen by
# mp s['record_data']
# Step 5) copy the values to the python file for practical 3

# The s['record_data'] is a list of three array (see edukit_mp.py):
#supervisory['record_data'] = [
#    array.array('i',[0 for _ in range(supervisory['record_num_samples'])]),
#    array.array('i',[0 for _ in range(supervisory['record_num_samples'])]),
#    array.array('f',[0. for _ in range(supervisory['record_num_samples'])]),
#    ]
# the first one is the stepper motor signal
# the second one the encoder signal
# the third one is the control signal (the step-like signal)

# In this practical only the encoder signal and the control signal are needed.

# Adjust the encoder signal array such that it is in the following (numpy array) form:
y = np.array([89, 89, 92, 91, 90, 91, 90, 88, 84, 82, 80, 76, 71, 67, 63, 57, 53, 48, 42, 34, 28, 22, 16, 8, 3, -4, -12, -16, -23, -31, -35, -44, -48, -52, -59, -62, -68, -70, -75, -80, -80, -83, -86, -88, -87, -88, -90, -88, -88, -87, -86, -83, -80, -78, -75, -71, -67, -63, -59, -53, -50, -45, -38, -31, -24, -18, -14, -7, -1, 3, 10, 17, 19, 26, 34, 36, 37, 23, 16, 13, 2, -4, -9, -21, -26, -32, -44, -45, -53, -63, -65, -72, -77, -84, -86, -89, -97, -98, -100, -102, -106, -105, -106, -106, -106, -105, -102, -101, -98, -94, -89, -86, -82, -77, -72, -66, -60, -53, -45, -39, -32, -24, -18, -11, -3, 3, 10, 19, 24, 31, 39, 44, 50, 56, 62, 65, 69, 75, 78, 81, 85, 88, 89, 89, 92, 92, 92, 90, 90, 89, 86, 83, 81, 77, 72, 68, 65, 60, 54, 48, 44, 36, 30, 25, 17, 11, 5, -3, -8, -14, -22, -27, -34, -41, -46, -54, -51, -38, -34, -30, -20, -13, -9, 1, 7, 12, 23, 26, 32, 40, 42, 50, 53, 57, 63, 65, 71, 71, 76, 77])

# Do the same for the control signal:
u = np.array([-200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0, -200.0])


# Run the following System identification code to get the model of the system:

N = len(u)           # number of samples
h = 0.01             # sampling time 
td = h*np.arange(N)  # discrete time instants


def param2ss(x,h):
    # helper function to get the state-space matrices out of the
    # optimization vector x (h is the sampling time)
    a,b,c,d,e=x # model and initial state parameters to optimize
    A = np.array([[0.,1.],[a*(-53), b*(-0.118)]])
    B = np.array([[0.],[c*(-3.0)]])
    C = np.array([[0.,1.]])
    D = np.array([[0.]])
    Ad,Bd,Cd,Dd = c2d_zoh(A,B,C,D,h)
    x0 = np.array([d,e])
    return Ad,Bd,Cd,Dd,x0

def func(x,u,y,h):
    # helper function for the optimization, given the
    # parameter vector x, the input-signal u, output-signal y
    # and the sampling time h, the error between the measured output
    # and the model-based simulated output is to be minimized
    Ad,Bd,Cd,Dd,x0 = param2ss(x,h)
    ye = sim(Ad,Bd,Cd,Dd,u,x0)  # simulated output
    return np.linalg.norm(y-ye) # cost-value to be minimized

# System identification step:
# Estimate the discrete-time state-space matrices and the initial-state
# that fit best with the recorded input/output data
# The function func defined above is to be minimized by function minimize from scipy.optimize:
x_init = np.array([1.,1.,1.,1.,y[0]])
other_func_args = (u,y,h)
result = minimize(func,x_init,other_func_args)
Ad,Bd,Cd,Dd,x0 = param2ss(result['x'],h)

# simulate the output of the model
ye = sim(Ad,Bd,Cd,Dd,u,x0)

# Step 7) Calculate the state-feedback gain L such that the closed-loop poles are both in 0.8, use the function place(!)

# Step 8) Calculate the observer gain K such that the observer-error poles are both in 0.8, use the function place(!)

# Step 9) Calculate the state-space controller matrices by:
Actrl = Ad-K@Cd-Bd@L
Bctrl = K
Cctrl = -L
Dctrl = np.zeros((1,1))

# Step 10) Create the closed-loop system of edukit pendulum with controller by:
# Note the positive feedback, because the negative value is already in Cctrl(!)
Afb,Bfb,Cfb,Dfb = ss_feedback(Ad,Bd,Cd,Dd,Actrl,Bctrl,Cctrl,Dctrl,np.array([+1]))

# Step 11) Simulate the closed-loop system with the original control signal u as input
#          and plot both the uncontrolled encoder signal (y) and the controlled one in
#          one figure.
#          Does the controller work?
#yec_uc = sim(Afb,Bfb,Cfb,Dfb,u)
#yec = yec_uc#[0,:]
#uc = yec_uc[1,:]


# Following steps are optional (i.e. implement the state-space controller and test the results):
# Step 12) Make sure you have the micropython with ulab firmware on the microcontroller. Ulab contains
# fast and minimal version of numpy to do matrix compuations on the microcontroller.
# You can check this by importing ulab either from the repl in rshell (do: "rshell -p COM4 repl" and
# then "import ulab"), or from the edukit_pc prompt (do: "mp import ulab").
# If you get an import error, you first need to flash the micropython with ulab. You can compile this
# from source, as explained on https://github.com/v923z/micropython-ulab#stm-based-boards, but a
# compiled hex-file is available from Brighspace. You can program the microcontroller with this file
# using the STM32CubeProgrammer (https://www.st.com/en/development-tools/stm32cubeprog.html) or ask
# the instructor (who does the deploy-stlink approach as explained on
# https://github.com/micropython/micropython/tree/master/ports/stm32).

# Step 13) Add the following StateSpace class definition to ucontrol.py
# and compile the file with mpy-cross at the command prompt (mpy-cross can by installed by pip!):
# mpy-cross -march=armv7emsp ucontrol.py
class StateSpace():
    def __init__(self,get_sensor,set_actuator,sampling_time_ms,A,B,C,run=False,supervisory={}):
        self.get_sensor = get_sensor
        self.set_actuator = set_actuator
        self.sampling_time_ms = sampling_time_ms
        self.A = A
        self.B = B
        self.C = C
        self.run = run
        self.x = np.array([[0.],[0.]])
        self.u = np.array([[0.]])
        self.sample = [0, 0, 0.]
        self.gain = 0.
        self.supervisory = supervisory

    async def control(self):
        self.y = self.get_sensor()
        
        if self.run:
            self.x[:] = np.dot(self.A,self.x)+self.B*self.y
            self.u[:] = np.dot(self.C,self.x)
            self.set_actuator(self.gain * self.u[0,0])
            
        self.sample[1] = self.y
        self.sample[2] = self.u[0,0]

# Step 14) Add the state-space controller matrices to the ctrlparam dictionary in edukit_mp.py:
# You may want to print them first by
print(f"ctrlparam['A'] = np.{Actrl.__repr__()}")
print(f"ctrlparam['B'] = np.{Bctrl.__repr__()}")
print(f"ctrlparam['C'] = np.{Cctrl.__repr__()}")
# and copy the printed output to edukit_mp.py.

# Step 15) Add a state-space controller object to edukit_mp.py, that should replace pid, by:
state_space = StateSpace(enc.value,set_period_direction,ctrlparam['sampling_time_ms'],ctrlparam['A'],ctrlparam['B'],ctrlparam['C'],False,supervisory)
# make sure to do this after the definition of the Encoder object enc!
# Also change the control task in the async definition main():
#    #control_task = asyncio.create_task(control(pid))
#    control_task = asyncio.create_task(control(state_space))    

# Step 16) Compile edukit_mp.py by
# mpy-cross -march=armv7emsp edukit_mp.py

# Step 17) Copy the new mpy files to the microcontroller with rshell by:
# rshell -p COM4 cp ucontrol.mpy /flash/
# rshell -p COM4 cp edukit_mp.mpy /flash/


# Step 18) In edukit_pc.py (so the PC version!), change the value of command in the plotter function by
#    #command = "pid.sample"
#    command = "state_space.sample"    

# Step 19) Start edukit_pc.py and check if the plotter shows the encoder value (note, the rotor angle is
# not shown because state_space.sample[0] is not updated in the controller (if you want, you can add it by changing the code).

# Step 20) Turn on the controller by changing its "run" attribute.

# Step 21) Verify if the control-signal is of "reasonable" size and not exploding.
# If so verify if the controller is implemented correctly.
# If that's the case, design a more conservative controller by moving the state-feedback and observer poles close to the unit-circle, and repeat the previous steps.

# Step 22) If the control signal is OK, change the "gain" attribute to 1, and verify if the controller stabilizes the pendulum.


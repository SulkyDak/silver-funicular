class PID:
    def __init__(self, P=1, I=1, D=1):
        self.P=P
        self.I=I
        self.D=D
        self.signal_values=[]
        self.area=0
    def proportion(self): # calculate proportional gain
        signal=self.signal_values
        weight=self.P
        if(len(signal)>1):
            result=signal[1]*weight
        else:
            result=signal[0]*weight
        return result
    def integral(self):   # calculate integral gain
        signal=self.signal_values
        weight=self.I
        if(len(signal)>1):
            area=(signal[0]+signal[1])/2
        else:
            area= 0
        self.area= self.area+ area
        result= self.area*weight
        return result
    def derivative(self): # calculate derivative gain
        signal=self.signal_values
        weight=self.D
        if(len(signal)>1):
            result= (signal[1]-signal[0])*weight
        else:
            result=0
        return result
    def signal(self, a):  # pass the error and calculate the output
        if(len(self.signal_values)>1):
            self.signal_values.pop(0)
            self.signal_values.append(a)
        else:
            self.signal_values.append(a)
        result=self.proportion()+ self.integral()+ self.derivative()
        return result


import gym
import ballbeam_gym
from matplotlib import pyplot as plt
kwargs = {'setpoint': 0,         # set the reference point as 0
          'timestep': 0.05, 
          'beam_length': 1.0,
          'max_angle': 0.5,
          'init_velocity': 0.5,
          'max_timesteps': 100}
env = gym.make('BallBeamSetpoint-v0', **kwargs)
env.reset()
#print(env.action_space)
# action space is restricted to (-0.5, 0.5) and 1, where the continuos range represents the angle by which is beam is rotated and 1 represents no action
#print(env.observation_space)
# observation space includes beam angle,ball position,ball velocity, setpoint position. setpoint position is set to 0 manually
controller=PID(1,0.0001,2) 
action=-0.5

angle=[]
pos=[]
for _ in range(100):
    
    observation, reward, done, info=env.step(action)
    err=controller.signal(observation[1]) # send the value of current position/error and get the converted signal
    action=err
    angle.append(observation[0])
    pos.append(observation[1])
env.close()

plt.subplot(2,2,1)
plt.title('ball position')
plt.xlabel('timestep')
plt.plot(pos)
plt.subplot(2,2,2)
plt.title('beam angle')
plt.xlabel('timestep')
plt.plot(angle)
plt.savefig('pidgraph3.png')
plt.savefig('pidgraph.png')
# graph1 used initial value of action as 0
# graph2 used initial value of action as 0.5
# graph3 used initial value of action as -0.3

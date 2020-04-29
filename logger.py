import matplotlib.pyplot as plt

import numpy as np

import serial

import time


Fs = 100.0;  # sampling rate

Ts = 10.0/Fs; # sampling interval

t = np.arange(0,10,Ts) # time vector; create Fs samples between 0 and 1.0 sec.

X = np.arange(0,10,Ts) # signal vector; create Fs samples

Y = np.arange(0,10,Ts) 

Z = np.arange(0,10,Ts)
Larger_5cm = np.arange(0,10,Ts)


serdev = '/dev/ttyACM0'

s = serial.Serial(serdev,115200)

for a in range(0, int(Fs)):

    line=s.readline() # Read an echo string from K66F terminated with '\n'
    
    linex = line[0:9]
    X[a] = float(linex)

    liney = line[9:18]
    Y[a] = float(liney)

    linez = line[18:27]
    Z[a] = float(linez)

directionx = 0
directiony = 0
displacementx = np.arange(0,10,Ts)
displacementy = np.arange(0,10,Ts)

for i in range(100):
    if(X[i]<0 && directionx==0):
        if(i==0):
            displacementx[i] = 0.5*9.8*abs(X[i])*(0.01)*(0.01)*100
        else:
            displacementx[i] = displacementx[i-1]+0.5*9.8*abs(X[i])*(0.01)*(0.01)*100
    elif (X[i]>0 && directionx==0):
        displacementx[i] = 0
        directionx = 1
    elif (X[i]<0 && directionx==1):
        displacementx[i] = 1
        directionx = 0
    elif (X[i]>0 && directionx==1):
        if(i==0):
            displacementx[i] = 0.5*9.8*abs(X[i])*(0.1)*(0.1)*100
        else:
            displacementx[i] = displacementx[i-1]+0.5*9.8*abs(X[i])*(0.1)*(0.1)*100

for i in range(100):
    if(Y[i]<0 && directiony==0):
        if(i==0):
            displacementy[i] = 0.5*9.8*abs(Y[i])*(0.01)*(0.01)*100
        else:
            displacementy[i] = displacementy[i-1]+0.5*9.8*abs(Y[i])*(0.1)*(0.1)*100
    elif (Y[i]>0 && directiony==0):
        displacementy[i] = 0
        directiony = 1
    elif (Y[i]<0 && directiony==1):
        displacementy[i] = 1
        directiony = 0
    elif (Y[i]>0 && directiony==1):
        if(i==0):
            displacementy[i] = 0.5*9.8*abs(Y[i])*(0.01)*(0.01)*100
        else:
            displacementy[i] = displacementy[i-1]+0.5*9.8*abs(Y[i])*(0.1)*(0.1)*100           
    
for i in range(100):
    if(abs(displacementx[i])>5 or abs(displacementy[i])>5):
        Larger_5cm[i] = 1
    else:
        Larger_5cm[i] = 0


fig, ax = plt.subplots(2, 1)

ax.plot(t,X,t,Y,t,Z)

ax.legend(('x','y','z'))

ax.set_xlabel('Time')

ax.set_ylabel('Acc Vector')

ax[1].stem(t,Larger_5cm,'g') # plotting the spectrum

ax[1].set_xlabel('Time')

ax[1].set_ylabel('Larger_than_5cm')

plt.show()

s.close()
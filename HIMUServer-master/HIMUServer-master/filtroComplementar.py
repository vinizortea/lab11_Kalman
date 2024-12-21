#===============================================================================
#
# MIT License
#
# HyperIMU Server (HIMU Server)
# Copyright (c) [2020] [Sebastiano Campisi - ianovir]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#===============================================================================

import math
import numpy as np
import matplotlib.pyplot as plt

from HIMUServer import HIMUServer

x_acc = []
y_acc = []
z_acc = []

x_gyro = []
y_gyro = []
z_gyro = []

time_step = 0.1
angulo = 0
#An example of listener implementation.
class SimplePrintListener:

    def __init__(self, serverInstance):
        self.__server = serverInstance
    		
    def notify (self, sensorData):
        global angulo
		#Customize the notify method in order to elaborate data
		# sensorData contains String values (see HIMUServer.__extractSensorData())
        #HIMUServer.printSensorsData(sensorData)
		#for a string-to-float conversion, try HIMUServer.strings2Floats()
        for sensors in sensorData:
            sensor_1 = HIMUServer.strings2Floats(sensors[0])
            sensor_2 = HIMUServer.strings2Floats(sensors[1])

            x_acc.append(sensor_1[0])
            y_acc.append(sensor_1[1])
            z_acc.append(sensor_1[2])

            x_gyro.append(sensor_2[0])
            y_gyro.append(sensor_2[1])
            z_gyro.append(sensor_2[2])
        
        x1,y1,z1 = sensor_1
        x2,y2,z2 = sensor_2

        if(y1 != 0):
            angulo = (0.98*(angulo + z2*time_step) + 0.02*(math.atan(x1/y1)))
            angulo_graus = angulo*57.296
            print(angulo_graus)

#HIMUServer instance:
myHIMUServer = HIMUServer()

#Creating listener and adding it to the server instance:
myListener = SimplePrintListener(myHIMUServer)
myHIMUServer.addListener(myListener)

#Change the timeout (in seconds) :
myHIMUServer.timeout = 2

#Launch acquisition via TCP on port 2055:
#myHIMUServer.start("TCP", 2055)

#Launch acquisition via UDP on port 2055:
myHIMUServer.start("UDP", 2055)

#Launch acquisition from local file:
# myHIMUServer.start("FILE", "HIMU-filetest.csv")


plt.figure(num=0,dpi=120)
plt.plot(x_acc, color="blue")
plt.plot(y_acc, color="green")
plt.plot(z_acc, color="red")
plt.show()

plt.figure(num=1,dpi=120)
plt.plot(x_gyro, color="blue")
plt.plot(y_gyro, color="green")
plt.plot(z_gyro, color="red")
plt.show()
# I2C Control
#
# This example shows how to use the i2c bus on your OpenMV Cam by dumping the
# contents on a standard EEPROM. To run this example either connect the
# Thermopile Shield to your OpenMV Cam or an I2C EEPROM to your OpenMV Cam.

from pyb import I2C
import mcu
from micropython import const
import time

i2c = I2C(3, I2C.MASTER, baudrate=100000)
print(i2c)
buf = bytearray(1)
temp = 7
while(1):
    temp = temp + 1
    print('write %d'%temp)
    i2c.mem_write(temp,0x68,0x6b) #value:5, slave add:0x68, addres:0x6b
    print('read back %s'%i2c.mem_read(1,0x68,0x6b))
    mem_buf = i2c.mem_read(1,0x68,0x75)
    print('mem_read from MPU%s'%mem_buf)
    i2c.send(0x75,addr=0x68)
    i2c.recv(buf,addr=0x68)
    print('recv from MPU%s'%buf)
    #time.sleep(200)

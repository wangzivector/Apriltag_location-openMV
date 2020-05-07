# Untitled - By: Lenovo - 周日 8月 11 2019

from pyb import SPI, Pin
pin4=Pin("P3",Pin.IN)
pin3=Pin("P4",Pin.OUT)
count=0
while(True):
    count+=1
    if(count>10):
        count=0
        pinvalue=pin3.value()
        print(pinvalue)
        pin4.value(pinvalue)


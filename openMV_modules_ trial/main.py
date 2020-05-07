import sensor, image, time,lcd,pyb
from pyb import UART
from pyb import Pin
uart = UART(4, 115200)
clock = time.clock()
smallsize=5
red_threshold =(0, 92, 24, 61, -21, 48)
RGB_gain = (-6, -6, -5)
num=0
prenum=0
prex=0
prey=0
prea=0
flag=0
ledb = pyb.LED(3)
ledg = pyb.LED(2)
ledr = pyb.LED(1)
command=0;
buf=b'00000000'
#f_l=0
#f_r=0
#b_l=0
#b_r=0
#speed_f=0
#speed_b=0
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_framerate(0<<9|1<<12)
sensor.set_auto_exposure(False,500)
sensor.set_contrast(0)
sensor.set_brightness(-3)
sensor.set_saturation(1)
sensor.set_auto_gain(False,10)
sensor.set_auto_whitebal(False,RGB_gain)
sensor.skip_frames(time = 2000)
while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([red_threshold], x_stride=2, y_stride=2, invert=False, area_threshold=6, pixels_threshold=6, merge=True, margin=5,roi=[0,60,320,195] )
    if blobs:
        for b in blobs:
            max_blob=find_max(blobs)
            if (max_blob[2]*max_blob[3]>smallsize):
                ledb.off()
                ledr.on()
                x=max_blob.cx()
                y=max_blob.cy()
                if (max_blob.area()<prea*9/10):
                    y=prey
                    x=prex
                    prenum=prenum+1
                else:
                    prea=max_blob.area()
                    prey=y
                    prex=x
                    prenum=0
                if(prenum>=3):
                    prenum=0
                    prea=0
                num=0
                flag=0
                xl=(x&0xff)
                xh=(x>>8&0xff)
                yl=(y&0xff)
                yh=(y>>8&0xff)
                uart.writechar(0xFC)
                uart.writechar(xh)
                uart.writechar(xl)
                uart.writechar(yh)
                uart.writechar(yl)
                uart.writechar(0xFE)
            else:
                num=num+1
    else:
        num=num+1
    if num>=5 :
        prea=0
        ledb.on()
        ledr.off()
        uart.writechar(0xFC)
        uart.writechar(0x00)
        uart.writechar(0x00)
        uart.writechar(0x00)
        uart.writechar(0x00)
        uart.writechar(0xFE)
        if uart.any():
            buf=uart.read(8)
            if buf[0]==97 and buf[7]==98:
                command=1
            if buf[0]==97 and buf[7]==99:
                command=2
            if buf[0]==97 and buf[7]==100:
                command=3
        if command==3:
            f_l=buf[1]
            f_r=buf[2]
            b_l=buf[3]
            b_r=buf[4]
            speed_f=buf[5]
            speed_b=buf[6]
            file_handle = open('1.txt', mode='w')
            str='%d,%d,%d,%d,%d,%d' % (buf[1],buf[2],buf[3],buf[4],buf[5],buf[6])
            file_handle.write(str)
            file_handle.close()
        if command==1:
            file_handle = open('1.txt', mode='r')
            frd=file_handle.read()
            frd_l=frd.split(',')
            f_l=int(frd_l[0])
            f_r=int(frd_l[1])
            b_l=int(frd_l[2])
            b_r=int(frd_l[3])
            speed_f=int(frd_l[4])
            speed_b=int(frd_l[5])
            f_l=(f_l&0xff)
            f_r=(f_r&0xff)
            b_l=(b_l&0xff)
            b_r=(b_r&0xff)
            speed_f=(speed_f&0xff)
            speed_b=(speed_b&0xff)
            uart.writechar(0xFD)
            uart.writechar(f_l)
            uart.writechar(f_r)
            uart.writechar(b_l)
            uart.writechar(b_r)
            uart.writechar(speed_f)
            uart.writechar(speed_b)
            uart.writechar(0xFE)
            file_handle.close()
        flag=1

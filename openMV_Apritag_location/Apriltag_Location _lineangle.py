# AprilTags Location
import time
from pyb import UART
from pyb import LED
import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

led = LED(3)
uart = UART(4, 115200, timeout_char=1000)
# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

#以下为在实测情况下的参数，对应的实际安装机械位置为：高度90cm  焦距水平距离Len64cm  镜头仰角26度（参考）
fmm = 3.6 #焦距
Len = 64 #焦点车中长
x = 0
y = 1
istag = 1
notag = 0
f_x = (fmm / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (fmm/ 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # (the image.w * 0.5)c_x is the image x center position in pixels.
c_y = 120 * 0.5 #(the image.h * 0.5),c_y is the image y center position in pixels.

enable_lens_corr = True
min_degree = 0
max_degree = 179
thetasave=[0 for x in range (0,5)]
thetacount=0
av_theta=0
av_count=3

def Find_realaxis(Istag, Id):
    int(Id)
    if Istag==istag:
        if Id%8 > 3:
            return (int(Id%4)*100+75, 375-50*int(Id/4))

        else:
            return ( int(Id%4)*100+25,375-50*int(Id/4))
    else:
        return ( int(Id%8)*50+25, 375-50*int(Id/8))

def vsLocation_to_realLocation(vsPosition):
    print("实际tag坐标:",Find_realaxis(istag, vsPosition[0]))
    if vsPosition[2] < 4:
        vsreal_dxdy =( vsPosition[1]*8.88, vsPosition[2]*11.44)
    else:
        vsreal_dxdy =( vsPosition[1]*8.88, vsPosition[2]*11.44)
    dxdy=Find_realaxis(istag, vsPosition[0])
    real_dxdy=( vsreal_dxdy[x]+dxdy[x], vsreal_dxdy[y]+dxdy[y])
    print("相对于tag的 实际图像中心坐标:",vsreal_dxdy,"实际图像中心坐标：",real_dxdy)
    return real_dxdy

def Image_to_vsLocation():
    img = sensor.snapshot()
    whole_preloca = [0 , 0 , 0, 0]
    for tag in img.find_apriltags(families=image.TAG25H9,fx=f_x, fy=f_y, cx=c_x, cy=c_y):
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        if tag.rotation() > math.pi:
            Rotation_co = tag.rotation() - 2*math.pi
        else:
            Rotation_co = tag.rotation()
        print_args = ()
        print(" " % print_args)
        #角度位置 逆变换
        anglA = math.atan( tag.x_translation() / tag.y_translation())#辅助斜向图像中心-tag角度
        if  tag.y_translation() >0:
            anglB =1.5*math.pi - anglA - Rotation_co#实际正直图像中心-tag角度
        else:
            anglB = -anglA- Rotation_co+0.5*math.pi
        L = math.sqrt(tag.x_translation()*tag.x_translation() + tag.y_translation()*tag.y_translation())
        dx = L*math.cos(anglB)
        dy = L*math.sin(anglB)
        vsPosition = (tag.id(), dx ,dy, (180*anglA) / math.pi, (180 * anglB) / math.pi,(180 * Rotation_co) / math.pi, L)
        #相对于tag，图像中心的实际相对坐标
        print("ID %d, dx:%f, dy:%f, anglA:%f  anglB:%f   rota:%f  L:%f"  % vsPosition)
        real_dxdy = vsLocation_to_realLocation(vsPosition) # 返回图像中心实际坐标

        #推算实际车坐标：
        whole_preloca[0] +=1
        whole_preloca[1] +=Rotation_co
        whole_preloca[2] +=real_dxdy[x]
        whole_preloca[3] +=real_dxdy[y]
    if whole_preloca[0] ==0:
        print("finding Apriltag...")
        led.toggle()
    else:
    #####################线识别偏角###############
        if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens..
        img.mean(2)
        for l in img.find_lines(threshold =1800, theta_margin = 5, rho_margin = 20):
            if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                img.draw_line(l.line(), color = (255, 0, 0))
                if l.y1()==0:
                    if l.theta()>90:
                        theta=180-l.theta()
                    else:
                        theta=-l.theta()
                else:
                    theta=90-l.theta()
                global thetacount
                if thetacount <av_count-1:
                    thetacount+=1
                else:
                    thetacount=0
                global thetasave
                thetasave[thetacount]=theta
                global av_theta
                for theta_sing in thetasave:
                    av_theta+=theta_sing
                av_theta/=av_count
    ############################################
        whole_preloca[1] = whole_preloca[1]/whole_preloca[0]#偏角
        whole_preloca[2] = whole_preloca[2]/whole_preloca[0]#横坐标
        whole_preloca[3] = whole_preloca[3]/whole_preloca[0]#纵坐标
        #print("平均实际图像中心坐标",whole_preloca)
        vsInvari_length = [Len * math.sin(math.pi+whole_preloca[1]), Len * math.cos(math.pi+whole_preloca[1])]
        #print("焦距水平距离换算结果：",vsInvari_length)
        Final_Position = [whole_preloca[2]+vsInvari_length[0] ,whole_preloca[3]+vsInvari_length[1]]
        print("final toy position: ",Final_Position)

        anglcar=int(whole_preloca[1]/math.pi*180)
        print(anglcar)
        print(av_theta)
        anglcar= 0.7*av_theta+0.3*anglcar
        if anglcar<0:
            anglcar=anglcar+360
        output_str="[%d,%d,%d]" % (int(Final_Position[0]),int(Final_Position[1]),anglcar)
        uart.write(output_str+'\r\n')
        led.toggle()
        print(output_str)
    img.draw_cross( 80, 60, color = (0 , 0, 200))


while(True):
    clock.tick()
    Image_to_vsLocation()
    print("////////////////////////////////     //////////////////////    ////////////////    //////")
    #print(clock.fps())




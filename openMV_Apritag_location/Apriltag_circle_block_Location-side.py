# AprilTags redbclock circle Location/side
from pyb import UART
from pyb import LED,Pin
import sensor, image, time, math,ustruct
import utime

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) #must turn this off to prevent image washout...
sensor.set_auto_whitebal(False) # must turn this off to prevent image washout...
clock = time.clock()

led = LED(3)
led2 = LED(2)
led3 = LED(1)
uart = UART(4, 115200, timeout_char=100)

#以下为在实测情况下的参数，对应的实际安装机械位置为：高度90cm  焦距水平距离Len64cm  镜头仰角26度（参考）
fmm = 2.8 #焦距
Len = 82 #焦点车中长
x_extraadd=0
x_corection =7.6
y_corection = 12
ddline=10
ddline2=15

x = 0
y = 1
istag = 1
notag = 0
f_x = (fmm / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (fmm/ 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # (the image.w * 0.5)c_x is the image x center position in pixels.
c_y = 120 * 0.5 #(the image.h * 0.5),c_y is the image y center position in pixels.

#circle
circle_reco_finish=1
Bthreshold=(0,110)
circle_finish=0
outputbit=8
outputlevel=0
k_cir_x=0.003#negative value
k_cir_y=0.1#positive value
k_cir_yy=0.3
k_cir_size_x=0.9#zoom rate_x
k_cir_size_y=1.35#zoom rate_x

cir_num=0
cir_number=[0.01*x for x in range(0,65)]#解决误识别和统计方便
output_circlenum=[0 for x in range(0,outputbit)]
output_circlenumlevel=[0 for x in range(0,outputbit)]

#block
blob_reco_finish=1
block_finish=0
short_value=2
long_value=10
blc_outputbit=32
blc_outputlevel=0
blc_number=[0.002*x for x in range(0, 129)]
output_blocknum=[0 for x in range(0, blc_outputbit)]
output_blocknumlevel=[0 for x in range(0, blc_outputbit)]
blc_gotnum=0

#line
min_degree = 0
max_degree = 179
av_count=3
thetasave=[0 for x in range (0,av_count)]
thetacount=0
av_theta=0
def Uart_rece_order():
    global circle_reco_finish
    global blob_reco_finish
    if uart.any():
        rece = uart.read(1)
        print(rece)
        if(rece==b'\xc0'):
            circle_reco_finish=1
            for con in range(65):
                cir_number[con]=0.01*con
            for con in range(outputbit):
                output_circlenum[con]=0
                output_circlenumlevel[con]=0
            cir_num=0
        if (rece==b'\xc1'):
            circle_reco_finish=0
        if(rece==b'\xb0'):
            for con in range(65):
                cir_number[con]=0.01*con
            for con in range(outputbit):
                output_circlenum[con]=0
                output_circlenumlevel[con]=0
            for con in range(129):
                blc_number[con]=0.002*con
            for con in range(blc_outputbit):
                output_blocknum[con]=0
                output_blocknumlevel[con]=0
            cir_num=0
            blob_reco_finish=1
            circle_reco_finish=1
        if (rece==b'\xb1'):
            blob_reco_finish=0
            circle_reco_finish=0


        #print("circle_reco_finish:",circle_reco_finish)
        #print("circle_reco_finish:",blob_reco_finish)
        #utime.sleep_ms(1000)

def Find_realaxis(Istag, Id):
    int(Id)
    if Istag==istag:
        if Id%8 > 3:
            return (int(Id%4)*100+75, 375-50*int(Id/4))

        else:
            return ( int(Id%4)*100+25,375-50*int(Id/4))
    else:
        return ( int(Id%8)*50+25, 375-50*int(Id/8))


def Image_to_vsLocation():
    img = sensor.snapshot()
    whole_preloca = [0 , 0 , 0, 0]
    circle_finish=0
    block_finish=0
    img_tag =  img.find_apriltags(families=image.TAG25H9,fx=f_x, fy=f_y, cx=c_x, cy=c_y)
    for tag in img_tag:
        print(tag)
        if tag.id()>31 :
            continue
        #print(tag.rotation())
        Rotation_co = tag.rotation()-1.5*math.pi#以y正方向为轴的包含正负角度，左负右正
        #print("Rotation_co",Rotation_co)
        #角度位置 逆变换
        anglA = math.atan( tag.x_translation()/ tag.y_translation())#辅助斜向图像中心-tag角度，正负以actan为准  以码为圆心，图像十字为目标
        if  tag.y_translation() >0:
            anglB =1.5*math.pi - anglA - Rotation_co#实际正直图像中心-tag角度
        else:
            anglB = -anglA+0.5*math.pi- Rotation_co
        L = math.sqrt(tag.x_translation()*tag.x_translation() + tag.y_translation()*tag.y_translation())
        dx = L*math.cos(anglB)#待修改
        dy = L*math.sin(anglB)
        if( dy<-4) :
            dy += 0.3
        if dx<-3:
            Rotation_co +=0.10
        if dx>3:
            Rotation_co -=0.03
        vsPosition = (tag.id(), dx ,dy, (180*anglA) / math.pi, (180 * anglB) / math.pi,(180 * Rotation_co) / math.pi, L)
        #相对于tag，图像中心的实际相对坐标
        print("ID %d, dx:%f, dy:%f, anglA:%f  anglB:%f   rota:%f  L:%f"  % vsPosition)
        if (len(img_tag) >2) and (tag.cy()<ddline) :
            continue
        if (len(img_tag) >1) and (tag.cy()<ddline2) :
            continue
        if (len(img_tag) >1) and (tag.cx()<ddline) :
            continue
        if (len(img_tag) >1) and (tag.cx()>(160-ddline)) :
            continue
        if Rotation_co>40 or Rotation_co<-40:
            continue

        img.draw_rectangle(tag.rect(), color = (255, 0, 255))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print("实际tag坐标:",Find_realaxis(istag, vsPosition[0]))
        vsreal_dxdy =( vsPosition[1]*x_corection+x_extraadd, vsPosition[2]*y_corection)
        dxdy=Find_realaxis(istag, vsPosition[0])
        real_dxdy=( -vsreal_dxdy[y]+dxdy[x], vsreal_dxdy[x]+dxdy[y])
        print("相对于tag的 实际图像中心坐标:",vsreal_dxdy,"实际图像中心坐标：",real_dxdy)

        #推算实际车坐标：
        whole_preloca[0] +=1
        whole_preloca[1] +=Rotation_co
        whole_preloca[2] +=real_dxdy[x]
        whole_preloca[3] +=real_dxdy[y]

    if whole_preloca[0] ==0:
        print("finding Apriltag...")
        led.toggle()
        led2.off()
    else:
        led2.on()
        whole_preloca[1] = whole_preloca[1]/whole_preloca[0]#偏角
        whole_preloca[2] = whole_preloca[2]/whole_preloca[0]#横坐标
        whole_preloca[3] = whole_preloca[3]/whole_preloca[0]#纵坐标
        print("平均实际图像中心坐标",whole_preloca)
        vsInvari_length = [Len * math.cos(whole_preloca[1]), Len * math.sin(whole_preloca[1])]
        print("焦距水平距离换算结果：",vsInvari_length)
        Final_Position = [whole_preloca[2]+vsInvari_length[0] ,whole_preloca[3]-vsInvari_length[1]]
        print("final toy position: ",Final_Position)
        if whole_preloca[1]>0:
            anglcar=int(whole_preloca[1]/math.pi*180)
        else:
            anglcar=int((2*math.pi+whole_preloca[1])/math.pi*180)
        if Final_Position[0]<0:
            Final_Position[0]=600-Final_Position[0]
        if Final_Position[1]<0:
            Final_Position[1]=600-Final_Position[1]
        output_str="[%d,%d,%d]" % (int(Final_Position[0]),int(Final_Position[1]),anglcar)
        global location_finish
        location_finish=1
        ##line angle
        global thetacount
        global av_count
        global av_theta
        for l in img.find_lines(threshold =4000, theta_margin = 5, rho_margin = 20):
            if (min_degree <= l.theta()) and (l.theta() <= max_degree) and  l.x1()==0 and( l.y1()>50 or l.y2()>50) :
                img.draw_line(l.line(), color = (255, 255, 0))
                theta=0
                if l.x1()==0:
                    theta=90-l.theta()
                if thetacount <av_count-1:
                    thetacount+=1
                else:
                    thetacount=0
                thetasave[thetacount]=theta
                for theta_sing in thetasave:
                    av_theta+=theta_sing
                av_theta/=av_count
                print(av_theta)
                if av_theta<-0.5:
                    av_theta_cor=360+av_theta
                else:
                    av_theta_cor=av_theta
                output_str="[%d,%d,%d]" % (int(Final_Position[0]),int(Final_Position[1]),av_theta_cor)
                print(av_theta_cor)
###########################################################################################
###########################################################################################
#next  is the redblock recognition#################################################################
    if(whole_preloca[0]>0) and blob_reco_finish==0:
        red = (21, 100, 24, 127, 0, 127)
        red_block=img.find_blobs([red], x_stride=short_value, y_stride=short_value, invert=False,\
        area_threshold=30,pixels_threshold=30, merge=False, margin=0)
        if len(red_block)>0:
            for blobs in red_block:
                yblob_location = blobs.y()
                xblob_location = blobs.x()
                #if (blobs.x()+blobs.w()/2)>80:
                    #xblob_location =blobs.x()+blobs.w()/2-80
                #else:
                    #xblob_location =-(blobs.x()+blobs.w()/2)+80
                if yblob_location >90 and 70<xblob_location <90:
                    continue
                if (blobs.w()>short_value and blobs.h()>long_value)or(blobs.w()>long_value and blobs.h()>short_value):
                    bb=[blobs.x()+blobs.w()*0.5-c_x,blobs.y()+blobs.h()*0.5-c_y]#中心点
                    print(blobs)
                    global k_cir_size_y
                    global k_cir_size_x
                    global k_cir_x
                    global k_cir_y
                    global k_cir_yy
                    if bb[1]<0:#y方向规整矫正
                        bb[1]=(bb[1]+bb[1]*k_cir_y)*k_cir_size_y
                    else:
                        bb[1]=(bb[1]-bb[1]*k_cir_yy)*k_cir_size_y

                    bb[0]=(bb[0]-bb[0]*bb[1]*k_cir_x )*k_cir_size_x#x方向规整矫正
                    print(bb)
                    print(whole_preloca[2],whole_preloca[3])
                    if (blobs.h()<blobs.w()):#竖向障碍
                        blc_posi = [whole_preloca[2]+bb[1]-25, whole_preloca[3]+bb[0]]
                        blcnum=int(blc_posi[0]/50)+int((400-blc_posi[1])/50)*8+64
                    else:#横向障碍
                        blc_posi = [whole_preloca[2]+bb[1], whole_preloca[3]+bb[0]+25]
                        blcnum=int(blc_posi[0]/50)+int((400-blc_posi[1])/50)*8
                    print(blcnum,blc_posi)
                    if blcnum<129:
                        blc_number[blcnum]+=1
                    else:
                        continue
                    img.draw_rectangle(blobs.rect(), color = (255, 255, 0), thickness = 1, fill = False)
            print(blc_number)
            te_blc_number=blc_number.copy()
            te_blc_number.sort(reverse=True)
            print(te_blc_number)
            countvalue=0
            while (countvalue < blc_outputbit):
                output_blocknum[countvalue]=blc_number.index(te_blc_number[countvalue])
                output_blocknumlevel[countvalue]=int (te_blc_number[countvalue])
                countvalue=countvalue+1
            block_finish=1
            print("detected blc_num:",output_blocknum)
            print("detected blc_numlevel:",output_blocknumlevel)
    ###########################################################################################
    ###########################################################################################
    ##now is time to circle the circle##################################################################
    #circle_value
    if(whole_preloca[0]>0) and circle_reco_finish==0:
        led3.on()
        k_cir_x=0.003#negative value
        k_cir_y=0.2#positive value
        k_cir_size_x=0.9#zoom rate_x
        k_cir_size_y=1.5#zoom rate_x
        #img.lens_corr(1.5)
        #img =img.rotation_corr(x_rotation = 20, y_rotation = 0, z_rotation = 0,  x_translation = 0,  \
        #y_translation = 0, zoom = 1)
        img.to_grayscale(copy=False)
        img.binary([Bthreshold])
        img.close(4)
        img.erode(2)
        img.negate()
        img =img.rotation_corr(x_rotation = 30, y_rotation = 0, z_rotation = 0,  x_translation = 0,  \
        y_translation = 0, zoom = 1)

        for c in img.find_circles( x_stride=1, y_stride=1,threshold =4000, x_margin = 10, y_margin = 10,\
         r_margin =10,r_min = 12, r_max = 18, r_step = 1):
            print(c)
            img.draw_cross(c.x(), c.y(),color = (0,0 , 255))
            img.draw_circle(c.x(), c.y(),c.r(),color = ( 255 ,0 ,0))
            cc=[c[0]-c_x,c[1]-c_y]#中心点

            if cc[1]<0:#y方向规整矫正
                cc[1]=(cc[1]+cc[1]*k_cir_y)*k_cir_size_y
            else:
                cc[1]=(cc[1]-cc[1]*k_cir_yy)*k_cir_size_y

            cc[0]=(cc[0]-cc[0]*cc[1]*k_cir_x )*k_cir_size_x#x方向规整矫正
            cir_posi = [whole_preloca[2]+cc[1], whole_preloca[3]+cc[0]]#真实坐标
            cirnum=int(cir_posi[0]/50)+int((400-cir_posi[1])/50)*8#解算号码位置
            print("raw axis(",c[0],",",c[1],")","corred to central axis:",cc,\
            "\n central real posi :(",whole_preloca[2],",",whole_preloca[3],")cir_posi:",cir_posi,"cirnum :",cirnum)


     #以下做筛选排除###############
            if cirnum<64:
                cir_number[cirnum]+=1
                global cir_num
                cir_num+=1
        print(cir_num,cir_number)
        if cir_num>outputbit*outputlevel:
            te_cir_number=cir_number.copy()
            te_cir_number.sort(reverse=True)
            countvalue=0
            while (countvalue < outputbit):
                output_circlenum[countvalue]=cir_number.index(te_cir_number[countvalue])
                output_circlenumlevel[countvalue]=int (te_cir_number[countvalue])
                countvalue=countvalue+1
            circle_finish=1
        else:
            print("waiting for ",outputbit,"circle location")
    else:
        led3.off()

#print number /uart
    if(whole_preloca[0]>0):#location uart sent
        if location_finish==1:
            print("output_str:",output_str)
            try:
                uart.write(output_str+'\r\n')
            except OSError as err:
                pass
        if circle_finish==1 and circle_reco_finish==0:#circle uart sent
            count=0
            for outnumlevel in output_circlenumlevel:
                if output_circlenumlevel[count]>=0xef:
                    output_circlenumlevel[count]=0xef
                count+=1
            print("output_circlenum:", output_circlenum)
            print("output_circlenumlevel:", output_circlenumlevel)
            circle_data=ustruct.pack("BBBBBBBBBBBBBBBBBBB" ,0xfe,\
            output_circlenum[0],output_circlenum[1],output_circlenum[2],output_circlenum[3],\
            output_circlenum[4],output_circlenum[5],output_circlenum[6],output_circlenum[7],0xfd,
            output_circlenumlevel[0],output_circlenumlevel[1],output_circlenumlevel[2],output_circlenumlevel[3],\
            output_circlenumlevel[4],output_circlenumlevel[5],output_circlenumlevel[6],output_circlenumlevel[7],0xfc)
            uart.write(circle_data)

        if block_finish==1 and blob_reco_finish==0:#blob uart sent
            count=0
            for outnumlevel in output_blocknumlevel:
                if output_blocknumlevel[count]>=0xef:
                    output_blocknumlevel[count]=0xef
                count+=1
            print("output_blocknum:", output_blocknum)
            print("output_blocknumlevel:", output_blocknumlevel)

            uart.writechar(0xfb)
            for i in range(32):
                uart.writechar(0xfa)
                uart.writechar(output_blocknum[i])
                uart.writechar(output_blocknumlevel[i])
            uart.writechar(0xf9)
        img.draw_cross( 80, 60, color = (0 , 0, 200))

while(True):
    clock.tick()
    led.toggle()
    Image_to_vsLocation()
    Uart_rece_order()
    print("////////////////////////////////////////////////////////////////////////////")
    print(clock.fps())




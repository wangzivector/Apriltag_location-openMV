## Apriltag implement (NXP RT1062 openMV) [library](https://github.com/openmv/apriltag)

This repository is a conclusion of finishing the visual task in **NXP National Smart Car Competition in China** , in which I won the national first prize with my teammates.

<div align="center">
<img src=".\PNG\car_frontside.jpg" height="30%" width="50%" />
</div>
<div align="center">
This is our moving platform
</div>

The computer vision task is mainly about how to locate the smart car in an Apriltag based map, which looks like this:
<div align="center">
<img src=".\PNG\map_of_the_competition.png" height="30%" width="50%" />
 </div>
I mainly focused on Apriltag recognition and find the location in a big map(4m*4m) with RT1062. Also I need to use low-resolution cameras to tell the smartcar position for loading and putting task. Following screen shots can demonstrate the work I have done.

<div align="center">
<img src=".\PNG\apriltag_task.png"  height="30%" width="50%" />
  </div>
<p align="center">Apriltag detection and car location</p>
<div align="center">
 <img src=".\PNG\circle_reco.png"  height="30%" width="50%" />
  </div>
<p align="center"> circles detection and location </p>
  
<div align="center">
 <img src=".\PNG\edge_dete.png"  height="30%" width="50%"  />
 </div>
<p align="center"> edge detection </p>
 

### [第十四届恩智浦杯全国大学生智能车竞赛](https://smartcar.cdstm.cn/)

#### The 14th National University  Students intelligent Car Race in China

#### this work was done in 2019.

The 14th National University  Students intelligent Car Race in China is one of the biggest engineer competitions in China which attracts thousands of undergraduates in Automation and EE majors to compete with each others.

 [Open design work](https://github.com/wangzivector/Apriltag_openMV_implement/blob/master/open%20report%20of%20work.pdf), which got the first prize, have released in this repository. Please feel free to contact with me when have questions or discussion.


# repository describe

* **openMV_Apritag_location** 

  contains the .py files that mainly about how to implement the openMV API in RT1062. which can tell the actual location of the car attached openMVs.  The difference of the four similar py files are attached in different directions.

* **openMV_modules_ trial**

  There are some implement about modules in openMV. Check them if you like.

* **open report of work.pdf**

  describe the design of the whole car. thank to my team.

  (Qiangqin Qiu \ Kainan Su \ Minjie Wang \ Chenglong Cai)

Also I have finished another vision work using NXP K66 chip with low-resolution camera to process gray images and other common vision tasks. If you are interested please contact me.



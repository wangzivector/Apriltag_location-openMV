# Find Lines Example

Bthreshold=(0,80)   #二值化阈值

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()


min_degree = 0
max_degree = 179


while(True):
    clock.tick()
    img = sensor.snapshot()

   # img1 = img1.lens_corr(1.0)
   # img1.binary([Bthreshold])

   # img1 =img1.rotation_corr(x_rotation = 38, \
      #                                    y_rotation = 0, \
        #                                  z_rotation = 0, \
          #                                x_translation = 0, \
            #                              y_translation = 0, \
              #                            zoom = 1)


    for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            img.draw_line(l.line(), color = (255, 0, 0))
            print(l)

    for r in img.find_rects(threshold = 10000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
        print(r)

    print("FPS %f" % clock.fps())


# A [theta+0:-rho] tuple is the same as [theta+180:+rho].

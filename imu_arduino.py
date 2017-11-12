#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
import datetime

ser = serial.Serial('COM4', 38400, timeout=1)

ax = ay = az = 0.0
yaw_mode = False


def read_data(previous_time, prev_x_acc, prev_y_acc, vx, vy, scanning_vals):
    global ax, ay, az
    ax = ay = az = 0.0

    prev_vx = vx
    prev_vy = vy
    # request data by sending a dot
    ser.write(b".")
    # while not line_done:
    line = ser.readline()

    angles = line.split(b", ")
    print(len(angles))
    if len(angles) == 4:
        print(angles)
        # Timestamp addition
        today = datetime.datetime.now()
        angles.append(today)



        ax = (angles[0])

        ay = (angles[1])

        az = (angles[2])
        if ax == -1 and az == -1:
            vx = 0
            vy = 0
            scanning_vals = False
        else:
            acc_x = float(ax) * 9.81 / 8192
            acc_y = float(ay) * 9.81 / 8192
            #print("raw x: {} \traw y: {}".format(ax, ay))
            #print("Acc. x: {}".format(float(acc_x)))
            #print("Acc: y: {}".format(float(acc_y)))
            if previous_time == None:
                diff = today
            else:
                diff = today - previous_time

            previous_time = today

            splitty = str(diff).split('.')
            diff = int(splitty[-1])
            #print(diff)
            previous_time = today

            # Let's calc the velocity

    print("Vel.X: {}".format(vx))
    print("Vel.Y: {}".format(vy))

    #print("diff: {}".format(diff))
    # v = 0.5 * diff * change in acceleration ( /1000/1000 to convert to seconds)
    #print("vx: {}".format(vx))
    if abs(float(ax)) > 0.01 and abs(float(ay)) > 0.01 and abs(float(az)) > 0.01:
        scanning_values = True
        vx += 0.5 * (diff/1000/1000) * (float(acc_x) + float(prev_x_acc))
                                # current value of X.acc
        vy += 0.5 * (diff/1000/1000) * (float(acc_y) + float(prev_y_acc))
        prev_x_acc = acc_x
        prev_y_acc = acc_y
        print("Vel X: {}".format(vx))
        print("Vel Y: {}".format(vy))


    return previous_time, prev_x_acc, prev_y_acc, vx, vy, scanning_vals


def loopy():
    global yaw_mode
    previous_time = None
    vx = 0
    vy = 0
    prev_y_acc = 0
    prev_x_acc = 0
    scanning_vals = True
    count = 0
    high_x = 0
    high_y = 0
    for i in range(7):
        previous_time, prev_x_acc, prev_y_acc, vx, vy, scanning_vals = read_data(previous_time, prev_x_acc, prev_y_acc, vx, vy, scanning_vals)

        print(scanning_vals)
        print("count: {}".format(count))
        if vx > high_x:
            high_x = vx
        if vy > high_y:
            high_v = vx
        count +=1
    return high_x, high_v

    ser.close()


if __name__ == '__main__': main()
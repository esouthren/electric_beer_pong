#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
import datetime

ser = serial.Serial('COM3', 38400, timeout=1)

ax = ay = az = 0.0
yaw_mode = False




def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()




def read_data(previous_time, prev_x_acc, prev_y_acc, vx, vy):
    global ax, ay, az
    ax = ay = az = 0.0

    prev_vx = vx
    prev_vy = vy
    # request data by sending a dot
    ser.write(b".")
    # while not line_done:
    line = ser.readline()

    angles = line.split(b", ")

    # Timestamp addition
    today = datetime.datetime.now()
    angles.append(today)

    if len(angles) == 4:

        ax = (angles[0])

        ay = (angles[1])

        az = (angles[2])



        acc_x = float(ax) * 9.81 / 8192
        acc_y = float(ay) * 9.81 / 8192
        print("raw x: {} \traw y: {}".format(ax, ay))
        print("Acc. x: {}".format(float(acc_x)))
        print("Acc: y: {}".format(float(acc_y)))
        if previous_time == None:
            diff = today
        else:
            diff = today - previous_time


        previous_time = today

        splitty = str(diff).split('.')
        diff = int(splitty[-1])
        print(diff)
        previous_time = today

        # Let's calc the velocity

        #print("Vel.X: {}".format(vx))
        #print("Vel.Y: {}".format(vy))


        #print("diff: {}".format(diff))
        # v = 0.5 * diff * change in acceleration ( /1000/1000 to convert to seconds)
        #print("vx: {}".format(vx))
        if abs(float(ax)) > 0.01 and abs(float(ay)) > 0.01 and abs(float(az)) > 0.01:
            vx += 0.5 * (diff/1000/1000) * (float(acc_x) + float(prev_x_acc))
                                    # current value of X.acc
            vy += 0.5 * (diff/1000/1000) * (float(acc_y) + float(prev_y_acc))
            prev_x_acc = acc_x
            prev_y_acc = acc_y
            print("Vel X: {}".format(vx))
            print("Vel Y: {}".format(vy))
        else:
            vx = 0;

    return previous_time, prev_x_acc, prev_y_acc, vx, vy


def main():
    global yaw_mode
    previous_time = None
    vx = 0
    vy = 0
    prev_y_acc = 0
    prev_x_acc = 0

    for i in range(1000000):
        previous_time, prev_x_acc, prev_y_acc, vx, vy = read_data(previous_time, prev_x_acc, prev_y_acc, vx, vy)


    ser.close()

if __name__ == '__main__': main()

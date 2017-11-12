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

def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()




def read_data(previous_time, prev_x_acc, prev_y_acc, vx, vy, g_ang_x, g_ang_y, g_ang_z, gx_previous, gy_previous, gz_previous):
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

    if len(angles) == 7:

        ax = (angles[0])

        ay = (angles[1])

        gx = float((angles[3])) / 65.5
        gy = float((angles[4])) / 65.5
        gz = float((angles[5])) / 65.5

        acc_x = float(ax) * 9.81 / 8192
        acc_y = float(ay) * 9.81 / 8192
        print("raw x: {} \traw y: {}".format(ax, ay))
        #print("Acc. x: {}".format(float(acc_x)))
        #print("Acc: y: {}".format(float(acc_y)))
        #print("Gyro. x: {}".format(float(gx)))
        #print("Gyro: y: {}".format(float(gy)))
        #print("Gyro: y: {}".format(float(gz)))

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

        #print("Vel.X: {}".format(vx))
        #print("Vel.Y: {}".format(vy))


        #print("diff: {}".format(diff))
        # v = 0.5 * diff * change in acceleration ( /1000/1000 to convert to seconds)
        #print("vx: {}".format(vx))
        if abs(float(acc_x)) > 0.01 and abs(float(acc_y)) > 0.01:
            vx += 0.5 * (diff/1000/1000) * (float(acc_x) + float(prev_x_acc))

            vy += 0.5 * (diff/1000/1000) * (float(acc_y) + float(prev_y_acc))


            prev_x_acc = acc_x
            prev_y_acc = acc_y
            print(vx)
            print(vx)

        else:
            vx = 0;
        g_ang_x += 0.5 * (diff / 1000 / 1000) * (float(gx) + float(gx_previous))
        g_ang_y += 0.5 * (diff / 1000 / 1000) * (float(gy) + float(gy_previous))
        g_ang_z += 0.5 * (diff / 1000 / 1000) * (float(gz) + float(gz_previous))
        #print("Angle X: {}".format(g_ang_x))
        #print("Angle Y: {}".format(g_ang_y))
        #print("Angle Z: {}".format(g_ang_z))


    return previous_time, prev_x_acc, prev_y_acc, vx, vy, g_ang_x, g_ang_y, g_ang_z, gx_previous, gy_previous, gz_previous


def main():
    global yaw_mode
    previous_time = None
    vx = 0
    vy = 0
    g_ang_x = 0
    g_ang_y = 0
    g_ang_z = 0

    prev_y_acc = 0
    prev_x_acc = 0
    gx_previous = 0
    gy_previous = 0
    gz_previous = 0

    while True:
        previous_time, prev_x_acc, prev_y_acc, vx, vy, g_ang_x, g_ang_y, g_ang_z, gx_previous, gy_previous, gz_previous = read_data(previous_time, prev_x_acc, prev_y_acc, vx, vy, g_ang_x, g_ang_y, g_ang_z, gx_previous, gy_previous, gz_previous)


    ser.close()

if __name__ == '__main__': main()
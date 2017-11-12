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




def read_data(previous_time):
    global ax, ay, az
    ax = ay = az = 0.0
    line_done = 0

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
        print((ax))
        print((ay))
        print((az))
        if previous_time == None:
            diff = 0
        else:
            diff = today - previous_time


        previous_time = today

        splitty = str(diff).split('.')
        print(splitty[-1])
        previous_time = today

    return previous_time


def main():
    global yaw_mode
    previous_time = None
    for i in range(10000):
        previous_time = read_data(previous_time)


    ser.close()

if __name__ == '__main__': main()

print("hello world");
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import time as tm
import msvcrt as m
import matplotlib.animation as animation
#import cmath as cm
from imu_arduino import *

def step(v, a):

    x = np.append(x, v_x)
    print(x);

def main(v_x, v_y, n):

    x = [0];
    y = [0];
    a_x = 0;
    a_y = -9.81;

    if((v_y**2 + (2 * a_y * y[0])) > 0):
        t = (-v_y - np.sqrt(v_y**2 + (2 * a_y * y[0])))/a_y;
    else:
        t = (-v_y + np.sqrt(v_y ** 2 + (2 * a_y * y[0]))) / a_y;
    tstep = t/n;
    print(t);
    print(tstep);
    x_max = v_x * t;
    print(x_max);
    x = np.linspace(0, x_max, n);
    print(x);

    for i in range(len(x)-1):
        y = np.append(y, y[0] + v_y * tstep*(i+1) + 0.5 * a_y * (tstep*(i+1))**2);

    print(x, y);

    fig, ax = plt.subplots()
    line, = ax.plot(x[0], y[0], color='k')
    #plt.show();
    #plt.xlim(0, 10)
    #plt.ylim(0, 6)
    #plt.show();
    bg = mpimg.imread(BACKGROUND);
    imgplot = plt.imshow(bg, aspect='auto', extent=(0, 6, 0, 2), alpha=1, zorder=-1);

    ball = mpimg.imread(BALL);
    ballplot = plt.imshow(ball, aspect='auto', extent=(x[0], x[0]+.3, y[0], y[0]+.3), alpha=1, zorder=1);

    logo = mpimg.imread('bee.png');
    logoplot = plt.imshow(logo, aspect='auto', extent=(4.7, 5.9, 1.4, 2.0), alpha=1, zorder=2, visible='off');

    one = mpimg.imread('100.png');
    oneplot = plt.imshow(one, aspect='auto', extent=(1, 4, .5, 2), alpha=1, zorder=0);
    oneplot.set_visible(not fig.get_visible())

    bicep = mpimg.imread('bicep.png');
    bicepplot = plt.imshow(bicep, aspect='auto', extent=(1.5, 1.5, 2, 1.4), alpha=1, zorder=1);
    bicepplot.set_visible(not fig.get_visible())

    ok = mpimg.imread('ok.png');
    okplot = plt.imshow(ok, aspect='auto', extent=(2, 3, 1, 1.4), alpha=1, zorder=5);
    okplot.set_visible(not fig.get_visible())

    def update(i, x, y, line):
        line.set_data(x[:i], y[:i])
        line.axes.axis([0, 6, 0, 2])

        ballplot.set_extent((x[i], x[i]+.5, y[i], y[i]+.2));
        tool = np.random.rand();
        oneplot.set_extent((1*tool,4*tool,.5*tool, 2*tool))

        if(x[i] > 2.2 and x[i] < [4] and y[i] < 0.5):
            print("WINNER!!")
            oneplot.set_visible(fig.get_visible());
            bicepplot.set_visible(fig.get_visible());
            okplot.set_visible(fig.get_visible());

        return ballplot,oneplot,bicepplot,okplot,

    #plt.ylabel('height /m')
    #plt.xlabel('displacement /m')
    #plt.grid(True);

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line], interval=1, blit=True, repeat=False)
    plt.show();

x = 0
y = 0
print("Welcome!")
bg = input("Which Background would you like? 0 = Meadow, 1 = Frat Party")
BACKGROUND = "lads.png"
BALL = "ball.png"
if bg == 0:
    BACKGROUND = "bg.png"
    BALL = "raspberry.png"



#x, y = loopy()
#print("GOT VALS!!")
main(x,y,50)

# main(5, 4, 50); # super slow # good simulation value


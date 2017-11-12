print("hello world");
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import time as tm
import matplotlib.animation as animation
#import cmath as cm

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
        #y = np.append(y, 0.5 * (v_y + a_y * tstep * (i+1) + v_y) * tstep * (i+1));
        #y = np.append(y, y[0] + v_y*tstep*(i+1) + 0.5*a_y*tstep*(i+1)**2);
        y = np.append(y, y[0] + v_y * tstep*(i+1) + 0.5 * a_y * (tstep*(i+1))**2);

    print(x, y);

    fig, ax = plt.subplots()
    line, = ax.plot(x[0], y[0], color='k')
    #plt.show();
    #plt.xlim(0, 10)
    #plt.ylim(0, 6)
    #plt.show();
    bg = mpimg.imread('bg.png');
    imgplot = plt.imshow(bg, aspect='auto', extent=(0, 30, 0, 15), alpha=1, zorder=-1);
    """
    for i in range(len(x)):
        plt.cla()
        line.set_data(x[:i], y[:i])

        ax.axis([0, 10, 0, 6])
        #ax.relim()
        #ax.autoscale_view(True, True, True)
        plt.draw()

        tm.sleep(0.01)
    """
    pi = mpimg.imread('raspberry.png');
    rasplot = plt.imshow(pi, aspect='auto', extent=(0, 3, 0, 1.5), alpha=1, zorder=1, visible='off');

    cloudx = np.linspace(0,7,len(x)/2);
    cloudx = np.append(cloudx, cloudx[::-1]);
    cloudy = 11+np.sin(x);
    print(cloudy)
    cloud = mpimg.imread('cloud.png');
    cloudplot = plt.imshow(cloud, aspect='auto', extent=(cloudx[0], cloudx[0]+3, cloudy[0], cloudy[0]+2), alpha=1, zorder=1);

    eyyy = mpimg.imread('eilidh.png');
    imgplot = plt.imshow(eyyy, aspect='auto', extent=(12, 15, 0, 3), alpha=1, zorder=2);

    def update(i, x, y, line):
        line.set_data(x[:i], y[:i])
        line.axes.axis([0, 30, 0, 15])

        #rasplot = plt.imshow(pi, aspect='auto', extent=(x[i], x[i]+3, y[i], y[i]+2), alpha=1, zorder=1);
        rasplot.set_extent((x[i], x[i]+3, y[i], y[i]+2));
        rasplot.set_extent((x[i], x[i] + 3, y[i], y[i] + 2));

        cloudplot.set_extent((cloudx[i],cloudx[i]+3,cloudy[i],cloudy[i]+2))
        #eyyy = imgplot.rotate(plt, 5)
        return rasplot,cloudplot

    #plt.ylabel('height /m')
    #plt.xlabel('displacement /m')
    #plt.grid(True);

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line], interval=10, blit=True)
    plt.show();

main(3.5, 12.8, 50);
# x, y, graph points
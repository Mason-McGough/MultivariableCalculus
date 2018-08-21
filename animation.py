"""
=====
Decay
=====

This example showcases a sinusoidal decay animation.
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

X = np.arange(-5, 5, 0.5)
Y = np.arange(-5, 5, 0.5)
nrows, ncols = X.shape[0], Y.shape[0]
rii = list(xrange(0, nrows))
cii = list(xrange(0, ncols))

Xm, Ym = np.meshgrid(X, Y)
Zm = np.zeros(Xm.shape[0])
X, Y, Z = np.broadcast_arrays(Xm, Ym, Zm)

f = lambda x, y, t : (x + t * np.sin(y), y + t * np.sin(x))

def data_gen(t=0):
    increment = 0.02
    cnt = 0
    max_cnt = 200
    while cnt < max_cnt:
        cnt += 1
        t += increment

        if t >= 1.0:
            t = 1.0
            increment = -increment
        elif t <= 0.0:
            t = 0.0
            increment = -increment

        x, y = f(X, Y, t)
        tx, ty, tZ = np.transpose(x), np.transpose(y), np.transpose(Z)

        xlines = [x[i] for i in rii]
        ylines = [y[i] for i in rii]
        zlines = [Z[i] for i in rii]

        txlines = [tx[i] for i in cii]
        tylines = [ty[i] for i in cii]
        tzlines = [tZ[i] for i in cii]

        lines = ([list(zip(xl, yl, zl))
                    for xl, yl, zl in zip(xlines, ylines, zlines)]
                + [list(zip(xl, yl, zl))
                    for xl, yl, zl in zip(txlines, tylines, tzlines)])

        yield lines


def init():
    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(-4.0, 4.0)
    ax.set_zlim(-1.0, 1.0)
    return surf,

# Create figure.
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_wireframe([], [], [], 
                         linewidth=1, antialiased=False,
                         rstride=25, cstride=25)
xdata, ydata, zdata = [], [], []
# plt.title('f(x, y)')


def run(data):
    # update the data
    lines = data
    surf.set_segments(lines)

    return surf,

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100,
                              repeat=False, init_func=init)

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Mason McGough'), bitrate=1800)
# ani.save('jacobian.mp4', writer=writer)

Writer = animation.writers['imagemagick']
writer = Writer(fps=12, metadata=dict(artist='Mason McGough'), bitrate=-1)
ani.save('jacobian.gif', writer=writer)

# plt.show()
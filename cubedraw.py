from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def drawcube(ax, x, y, z, clr):
    bottomx = [x[0], x[2], x[6], x[4], x[0]]
    bottomy = [y[0], y[2], y[6], y[4], y[0]]
    bottomz = [z[0], z[2], z[6], z[4], z[0]]
    topx = [x[1], x[3], x[7], x[5], x[1]]
    topy = [y[1], y[3], y[7], y[5], y[1]]
    topz = [z[1], z[3], z[7], z[5], z[1]]
    ax.plot3D(bottomx, bottomz, bottomy, color=clr)
    ax.plot3D(topx, topz, topy, color=clr)
    ax.plot3D(x[0:2], z[0:2], y[0:2], color=clr)
    ax.plot3D(x[2:4], z[2:4], y[2:4], color=clr)
    ax.plot3D(x[4:6], z[4:6], y[4:6], color=clr)
    ax.plot3D(x[6:8], z[6:8], y[6:8], color=clr)

x0 = [800, 800, 840, 840, 800, 800, 840, 840]
# x0 = [800, 840, 800, 840, 800, 840, 800, 840]

y0 = [20, 160, 20, 140, 20, 160, 20, 140]
# y0 = [20, 20, 20, 20, 160, 140, 160, 140]

z0 = [0, 0, 0, 0, 200, 200, 200, 200]
# z0 = [0, 0, 200, 200, 0, 0, 200, 200]

x1 = [0, 0, 800, 800, 0, 0, 800, 800]

y1 = [20, 160, 20, 160, 20, 140, 20, 140]

z1 = [200, 200, 200, 200, 240, 240, 240, 240]

x2 = [800, 800, 840, 840, 800, 800, 840, 840]

y2 = [20, 160, 20, 140, 20, 140, 20, 140]

z2 = [200, 200, 200, 200, 240, 240, 240, 240]
fig = plt.figure()
ax = Axes3D(fig)
drawcube(ax, x0, y0, z0, 'b')
drawcube(ax, x1, y1, z1, 'r')
drawcube(ax, x2, y2, z2, 'g')
# ax.plot3D(x0,z0,y0,'rx-')
# ax.plot3D(x1, z1, y1, 'bd-.')
# ax.plot3D(x2, z2, y2, 'g^-')

plt.gca().invert_zaxis()
plt.show()
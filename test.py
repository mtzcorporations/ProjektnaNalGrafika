import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore


## Create a GL View widget to display data
app = pg.mkQApp("GLSurfacePlot Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Difuzija')
w.setCameraPosition(distance=50)

g = gl.GLGridItem()
g.scale(1,1,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
w.addItem(g)
rows = 50
cols = 50
X=np.linspace(-10, 10, cols)
Y=np.linspace(-10, 10, rows)

p4 = gl.GLSurfacePlotItem(x=X,y=Y,shader='heightColor', computeNormals=False, smooth=False)
p4.shader()['colorMap'] = np.array(list(np.linspace(0, 1, 1000)))

#p4.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
w.addItem(p4)


print("2D heat equation solver")

plate_length = 50
max_iter_time = 10000

alpha = 2
delta_x = 1

delta_t = (delta_x ** 2)/(4 * alpha)
gamma = (alpha * delta_t) / (delta_x ** 2)

# Initialize solution: the grid of u(k, i, j)
u = np.empty((max_iter_time, plate_length, plate_length)) #snov1
v=np.empty((max_iter_time, plate_length, plate_length)) #snov2
# Initial condition everywhere inside the grid
u_initial = 0
v_initial = 0
# Boundary conditions
u_top = 10.0
u_left = 0.0
u_bottom = 0.0
u_right = 0.0

# Set the initial condition
u.fill(u_initial)
v.fill(v_initial)
for i in range(1, plate_length - 1, delta_x):
    for j in range(1, plate_length - 1, delta_x):
        u[0, i, j] = 1+random.randrange(0, 100, 100)
        v[0, i, j] = random.randrange(0, 1, 100)

def calculate():
    global p4,u,v

    for i in range(1, plate_length-1, delta_x):
        for j in range(1, plate_length-1, delta_x):
            u[1, i, j] = gamma * (u[0][i+1][j] + u[0][i-1][j] + u[0][i][j+1] + u[0][i][j-1] - 4*u[0][i][j]) \
                         + u[0][i][j] + (u[0][i][j]-v[0][i][j])*0.1 #R
            v[1, i, j] = gamma * (v[0][i + 1][j] + v[0][i - 1][j] + v[0][i][j + 1] + v[0][i][j - 1] - 4 * v[0][i][j]) \
                         + v[0][i][j] + (u[0][i][j]-v[0][i][j] + u[0][i][j]**2)*0.1 #R
    print("test ")
    p4.setData(z=u[1])
    u[0]=u[1]
    v[0] = v[1]


# Do the calculation here
#u = calculate(u)
timer = QtCore.QTimer()
timer.timeout.connect(calculate)
timer.start(30)

if __name__ == '__main__':
    pg.exec()

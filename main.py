from random import random

import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore


## Create a GL View widget to display data
app = pg.mkQApp("GLSurfacePlot Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
w.setCameraPosition(distance=50)

## Add a grid to the view
g = gl.GLGridItem()
g.scale(1,1,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
w.addItem(g)

## Animated example
## compute surface vertex data
rows = 100
cols = 100
x=np.linspace(-10, 10, cols)
y=np.linspace(-10, 10, rows)
## create a surface plot, tell it to use the 'heightColor' shader
## since this does not require normal vectors to render (thus we
## can set computeNormals=False to save time when the mesh updates)
p4 = gl.GLSurfacePlotItem(x = x, y = y, shader='heightColor', computeNormals=False, smooth=False)
p4.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
w.addItem(p4)


def randomMatrix():
    matrika = []
    for y in range(rows):
        arr = []
        for x in range(cols):
            arr.append(10 * random())
        matrika.append(arr)
    return np.array(matrika)
def dqdx_matrix(q_matrix):  #poracuna odvode matrike q_matrix po dx, tudi za 2. , n. odvode
    dqdx = []
    for y in range(1, rows - 1):
        dqdx_y = []
        for x in range(1, cols - 1):
            dqdx_y.append(((q_0[y][x - 1] - q_0[y][x]) / dx + (q_0[y][x + 1] - q_0[y][x]) / dx) / 2)
        dqdx.append(dqdx_y)
    return dqdx
def dqdy_matrix(q_matrix):  #poracuna odvode matrike q_matrix po dy
    dqdy = []
    for x in range(1, rows - 1):
        dqdy_x = []
        for y in range(1, cols - 1):
            dqdy_x.append(((q_0[y - 1][x] - q_0[y][x]) / dy + (q_0[y+1][x] - q_0[y][x]) / dy) / 2)
        dqdy.append(dqdy_x)
    return dqdy
def D_laplatz_q_dt(D,laplatz,dt):
    dq=[]
    for y in range(len(laplatz)):
        dq_x = []
        for x in range(len(laplatz[y])):
            dq_x.append(D*laplatz[y][x]*dt)
        dq.append(dq_x)
    return dq
def starting_q(cols, rows):
    q = []
    for y in range(rows):
        q_x = []
        for x in range(cols):
            if(cols/3 < x < 2*cols/3 and rows/3 < y < 2*rows/3):
                q_x.append(5)
            else:
                q_x.append(0)
        q.append(q_x)
    return q

def q_dq_sum(q,dq):
    qsum = []
    for y in range(len(q)):
        qsum_x=[]
        for x in range(len(q[y])):
            try:
                qsum_x.append(q[y][x]+dq[y][x])
            except:
                qsum_x.append(q[y][x])
        qsum.append(qsum_x)
    return qsum
iteration=0
dt = 0.1 #Delta čas
q_0 = starting_q(cols, rows) #začetno stanje koncentracije
dx = 20 / cols
dy = 20 / rows
D = -0.01
def update():
    global iteration,q_0
    dqdx = dqdx_matrix(q_0) #prvi odvod po x
    dqdy = dqdy_matrix(q_0) #prvi odvod po y
    d2qdx2 = dqdx_matrix(dqdx)  # drugi odvod po x
    d2qdy2 = dqdy_matrix(dqdy)  # drugi odvod po y

    laplatz=d2qdx2+d2qdy2
    dq = D_laplatz_q_dt(D,laplatz,dt)
    q_1 =  q_dq_sum(q_0,dq)

    p4.setData(z=np.array(q_1)) #update izrisa
    iteration+=1
    q_0=q_1  #posodobi prejšnje stanje
    print(iteration)


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)

if __name__ == '__main__':
    pg.exec()

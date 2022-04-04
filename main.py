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
X=np.linspace(-10, 10, cols)
Y=np.linspace(-10, 10, rows)
## create a surface plot, tell it to use the 'heightColor' shader
## since this does not require normal vectors to render (thus we
## can set computeNormals=False to save time when the mesh updates)
p4 = gl.GLSurfacePlotItem(x = X, y = Y, shader='heightColor', computeNormals=False, smooth=False)
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

def d2qdv2_fun(u_v1, u_v, u_v_1, dv):
    return (u_v1 - 2 * u_v + u_v_1) / (dv ** 2)
def d2qdv2_matrix(q):  #poracuna odvode matrike q_matrix po dy
    d2qdv2 = []
    for y in range(1, rows - 1):
        dqdv_y = []
        for x in range(1, cols - 1):
            dqdv_y.append(d2qdv2_fun(q[y][x+1],q[y][x],q[y][x-1],dx) + d2qdv2_fun(q[y+1][x],q[y][x],q[y-1][x],dy))

        d2qdv2.append(dqdv_y)
    return d2qdv2
def D_laplatz_q_dt(D,laplatz,dt):
    dq=[]
    for y in range(len(laplatz)):
        dq_y = []
        for x in range(len(laplatz[y])):
            dq_y.append(D*laplatz[y][x]*dt)
        dq.append(dq_y)
    return dq
def starting_q(cols, rows):
    q = []
    for y in range(rows):
        q_x = []
        for x in range(cols):
            if(cols/3 < x < 2*cols/3 and rows/3 < y < 2*rows/3):
                q_x.append(0.5)
            else:
                q_x.append(0)
        q.append(q_x)
    return q

def q_dq_sum(q,dq):
    qsum = []
    for y in range(len(q)):
        qsum_y=[]
        for x in range(len(q[y])):
            try:
                if(0<q[y][x]<1):
                    qsum_y.append(q[y][x]+dq[y][x])
                else:
                    qsum_y.append(q[y][x])
            except:
                qsum_y.append(q[y][x])
        qsum.append(qsum_y)
    return qsum
iteration=0

q_0 = starting_q(cols, rows) #začetno stanje koncentracije
dx = 20 / cols
dy = 20 / rows
D = 0.1
dt = 0.001
def update():
    global iteration,q_0

    laplatz = d2qdv2_matrix(q_0)
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

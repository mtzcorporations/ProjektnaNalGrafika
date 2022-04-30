import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph.examples
from PyQt5 import QtCore

#pyqtgraph.examples.run()

U=[]
v=None

app = pg.mkQApp("GLVolumeItem Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Reaction-diffusion system')
w.setCameraPosition(distance=200)

g = gl.GLGridItem()
g.scale(10, 10, 1)
w.addItem(g)

def get_color(U): #0 do 1
    #U=U/np.max(U)
    if (U>0.7):
        return [255*U,0,0,50]
    return [0,0,0,0] #RGBa

def create3D(d2):
    volume=[]
    for z in range(100):
        surface = []
        for y in range(100):
            line=[]
            for x in range(100):
                line.append(get_color(d2[z][y][x]))
            surface.append(line)
        volume.append(surface)
    return volume

def init(koncentracije):
    global U #koncentracije

    for k in koncentracije:
        k=create3D(k)
        k=np.array(k)
        U.append(k)
    show()

def show():
    global v

    v = gl.GLVolumeItem(U[0])  # x,y,z, RGBa
   # v.translate(-50, -50, -100)
    w.addItem(v)
    ax = gl.GLAxisItem()
    w.addItem(ax)

index=1
def update():
    global index
    if(index==len(U)):
        index=0
    v.setData(U[index])
    index+=1


timer = QtCore.QTimer()
def start():
    timer.timeout.connect(update)
    timer.start(1000)
    pg.exec()

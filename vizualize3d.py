import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph.examples
#yqtgraph.examples.run()



app = pg.mkQApp("GLVolumeItem Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Reaction-diffusion system')
w.setCameraPosition(distance=200)

g = gl.GLGridItem()
g.scale(10, 10, 1)
w.addItem(g)

def get_color(U): #0 do 1
    return [255*U,0,0,255*U] #RGBa

def create3D(d2):
    volume=[]
    for z in range(100):
        surface = []
        for y in range(100):
            line=[]
            for x in range(100):
                if(z==0):
                    line.append(get_color(d2[y][x]))
                else:
                    line.append(get_color(0))
            surface.append(line)
        volume.append(surface)
    return volume

def show2D(d2):
    d2=create3D(d2)
    d2=np.array(d2)
    v = gl.GLVolumeItem(d2)  # x,y,z, RGBa
    v.translate(-50, -50, -100)
    w.addItem(v)
    ax = gl.GLAxisItem()
    w.addItem(ax)
    pg.exec()
    print("frame")
def show3D(d2):
    v = gl.GLVolumeItem(d2)  #x,y,z, RGBa
    v.translate(-50,-50,-100)
    w.addItem(v)
    ax = gl.GLAxisItem()
    w.addItem(ax)
    pg.exec()


import pyqtgraph as pg
import pyqtgraph.opengl as gl



app = pg.mkQApp("GLVolumeItem Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Reaction-diffusion system')
w.setCameraPosition(distance=200)

g = gl.GLGridItem()
g.scale(10, 10, 1)
w.addItem(g)



def show3D(d2):
    v = gl.GLVolumeItem(d2)  #x,y,z, RGBa
    v.translate(-50,-50,-100)
    w.addItem(v)
    ax = gl.GLAxisItem()
    w.addItem(ax)

if __name__ == '__main__':
    pg.exec()

import numpy as np
import random

def init(n):
    u = np.ones((n + 2, n + 2))
    v = np.zeros((n + 2, n + 2))

    x, y = np.meshgrid(np.linspace(0, 1, n + 2), np.linspace(0, 1, n + 2))

    mask = (0.4 < x) & (x < 0.6) & (0.4 < y) & (y < 0.6)

    u[mask] = 0.50
    v[mask] = 0.25

    return u, v
def periodic_bc(u):
    u[0, :] = u[-2, :]
    u[-1, :] = u[1, :]
    u[:, 0] = u[:, -2]
    u[:, -1] = u[:, 1]
    return u

def laplacian(u):
    """
    second order finite differences
    """
    return (                  u[ :-2, 1:-1] +
             u[1:-1, :-2] - 4*u[1:-1, 1:-1] + u[1:-1, 2:] +
                          +   u[2:  , 1:-1] )

def grayscott(U,V ,Du, Dv, F, k):

    u, v = U[1:-1, 1:-1], V[1:-1, 1:-1]

    Lu = laplacian(U)
    Lv = laplacian(V)

    uvv = u * v * v
    u += Du * Lu - uvv + F * (1 - u)
    v += Dv * Lv + uvv - (F + k) * v

    U=periodic_bc(U)
    V=periodic_bc(V)

    return U,V


#fig, axes = plt.subplots(3, 3, figsize=(8, 8))

Du, Dv = .1, .05
F, k = 0.0545, 0.062
# We simulate the PDE with the finite difference
# method.
#K=[]
U, V = init(300)
def run():
    global U,V
    n = 40
    for i in range(n):
        # We compute the Laplacian of u and v.
        U,V=grayscott(U,V ,Du, Dv, F, k)
        V+=V*random.random()*0.003
    V_scaled = np.uint8(255 * (V - V.min()) / (V.max() - V.min()))
    return V_scaled
def frames(n):
    fr=[]
    for i in range(n):
        format_float = "{:.2f}".format(i / (n) * 100)
        print(format_float, "%")
        fr.append(run())
    return fr
    #return [run() for i in range(n)]

K=frames(200)
print(len(K))

print("hey")

#fig, ax = plt.subplots(1, 1, figsize=(8, 8))
#show_patterns(U, ax=ax)
#plt.show()
#print(u)
def get_colors(pix):
    if (pix > 0.7):
        return [255 * U, 0, 0, 255]
    return [122, 50, 50, 255]  # RGBa
def create2D( U):
    surface = []
    for y in range(120):
        line = []
        for x in range(100):
            line.append(get_colors(U[y][x]))
        surface.append(line)
    return surface



# K=[]
# for k in u:
#     k=create2D(k)
#     k=np.array(k)
#     K.append(k)

# importing Qt widgets
from PyQt5.QtWidgets import *

# importing system
import sys

# importing numpy as np
import numpy as np

# importing pyqtgraph as pg
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph.ptime as ptime


# Image View class
class ImageView(pg.ImageView):

    # constructor which inherit original
    # ImageView
    def __init__(self, *args, **kwargs):
        pg.ImageView.__init__(self, *args, **kwargs)


class Window(QMainWindow):

    def __init__(self,K):
        super().__init__()

        # setting title
        self.setWindowTitle("PyQtGraph")

        # setting geometry
        self.setGeometry(300, 300, 600, 500)

        # icon
        icon = QIcon("skin.png")

        # setting icon to the window
        self.setWindowIcon(icon)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # creating a widget object
        widget = QWidget()

        # creating a label
        label = QLabel("Geeksforgeeks Video")

        # setting minimum width
        label.setMinimumWidth(130)

        # making label do word wrap
        label.setWordWrap(True)

        # setting configuration options
        pg.setConfigOptions(antialias=True)

        # creating a graphics layout widget
        win = pg.GraphicsLayoutWidget()

        # adding view box object to graphic window
        view = win.addViewBox()

        ##lock the aspect ratio so pixels are always square
        view.setAspectLocked(True)

        # Create image item
        self.img = pg.ImageItem(border='w')

        # adding image item to the view box
        view.addItem(self.img)

        # Set initial view bounds
        view.setRange(QRectF(0, 0,500 , 500))

        #  Create random image
        self.data = K

        # helps in incrementing
        self.i = 0

        # getting time
        self.updateTime = ptime.time()

        # fps
        self.fps = 0

        # method to update the data of image
        def updateData():
            ## Display the data
            self.img.setImage(np.array(self.data[self.i]))
            #x=self.data[self.i]
            # creating new value of i
            self.i += 1
            print(self.i)
            if(self.i==len(self.data)-1):
                self.i=0
                #print("Tu",self.i
            # print(u)
            # creating a qtimer
            QTimer.singleShot(50, updateData)

            # getting current time
            now = ptime.time()

            # temporary fps
            fps2 = 1.0 / (now - self.updateTime)

            # updating the time
            self.updateTime = now

            # setting original fps value
            self.fps = self.fps * 0.9 + fps2 * 0.1

        # call the update method
        updateData()

        # Creating a grid layout
        layout = QGridLayout()

        # minimum width value of the label
        label.setMinimumWidth(130)

        # setting this layout to the widget
        widget.setLayout(layout)

        # adding label in the layout
        layout.addWidget(label, 1, 0)

        # plot window goes on right side, spanning 3 rows
        layout.addWidget(win, 0, 1, 3, 1)

        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window(K)

# start the app
sys.exit(App.exec())
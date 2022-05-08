import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation

a = 2.8e-4
b = 5e-3
tau = .1
k = -.005

size = 120  # size of the 2D grid
dx = 2. / size  # space step
T = 20.0  # total time
dt = .001  # time step
n = int(T / dt)  # number of iterations

U = np.ones([size, size])
#V=np.zeros([size, size])
#V[30:40,25:31]=1
#U = np.random.rand(size, size)
V = np.zeros([size,size])

V[0:10,0:10]=1
V[75:83,0:10]=1
V[60:68,0:10]=1
V[50:55,0:10]=1
V[30:40,0:10]=1

def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter) / dx**2

def show_patterns(U, ax=None,iter=0):
    ax.imshow(U, cmap=plt.cm.copper,
              interpolation='bilinear',
              extent=[-1, 1, -1, 1])
    ax.set_axis_off()
    fig.savefig(f'rd_{iter}.png')

#fig, axes = plt.subplots(3, 3, figsize=(8, 8))
step_plot = n // 200
# We simulate the PDE with the finite difference
# method.
def equation1(Uc,Vc,deltaU,deltaV):
    return Uc + dt * (a * deltaU + Uc - Uc ** 3 - Vc + k), Vc + dt * (b * deltaV + Uc - Vc) / tau
def equation2(A,B,deltaU,deltaV):
    y=1.6
    alfa=5.2
    lmb=2.5
    return -A*(-deltaU**(y/2)+1-A-alfa**2*A*B**2),-B*(-deltaV**(y/2)-lmb*B-alfa**2*A*B**2)
def equation3(A,B,deltaU,deltaV):

    lmb=0.05
    return lmb*deltaU
u=[]
print("zacetek",n)
for i in range(n):
    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)
    # We take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1]
    Vc = V[1:-1, 1:-1]
    # We update the variables.
    U[1:-1, 1:-1], V[1:-1, 1:-1] = equation2(Uc,Vc,deltaU,deltaV)
    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0, :] = Z[1, :]
        Z[-1, :] = Z[-2, :]
        Z[:, 0] = Z[:, 1]
        Z[:, -1] = Z[:, -2]

    # We plot the state of the system at
    # 9 different times.
    if i % step_plot == 0 and i < 200 * step_plot:
        u.append(np.copy(V))
        format_float = "{:.2f}".format(i / n * 100)
        print(format_float, "%")

        #ax = axes.flat[i // step_plot]
        #show_patterns(U, ax=ax,iter=i)
        #ax.set_title(f'$t={i * dt:.2f}$')
    #u.append(U)


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



K=[]
for k in u:
    k=create2D(k)
    k=np.array(k)
    K.append(k)

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

    def __init__(self,u):
        super().__init__()

        # setting title
        self.setWindowTitle("PyQtGraph")

        # setting geometry
        self.setGeometry(100, 100, 600, 500)

        # icon
        icon = QIcon("skin.png")

        # setting icon to the window
        self.setWindowIcon(icon)

        # calling method
        self.UiComponents()
        self.u=u
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
        view.setRange(QRectF(0, 0,150 , 150))

        #  Create random image
        self.data = u

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
            QTimer.singleShot(130, updateData)

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
window = Window(u)

# start the app
sys.exit(App.exec())
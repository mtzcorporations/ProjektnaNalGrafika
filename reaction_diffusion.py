
# import matplotlib.pyplot as plt
from math import *
# import matplotlib.pyplot as plt
from math import *

import numpy as np

a = 2.8e-6
b = 5e-5
tau = .001
k = -.00005
epsilon=1.5
b1=5e-5
b2=5e-5
size = 100  # size of the 2D grid
dx = 2. / size  # space step
T = 9.0  # total time
dt = .00005  # time step
n = int(T / dt)  # number of iterations


def init_StateRand():
    U = np.random.rand(size, size, size)
    V = np.random.rand(size, size, size)
    for z in range(len(U)):
        for y in range(len(U[z])):
            for x in range(len(U[z][y])):
                if (x < len(U) / 2):
                    U[z][y][x] = max(
                        [
                            0, min(
                            [
                                1, U[z][y][x] * 0.8 + (sin((x-50 *(x-50)/50) + sin((y-50) *(y-50)/50) + sin((z-50)*(z-50)/50))) / (
                                        (x / 20 -2 ) ** 2 + (y / 20 -2) ** 2 + (z / 20-2) ** 2 + 0.01)])])
                else:
                    U[z][y][x] = 0
    return U, V
def init(n):
    u = np.ones((n, n,n ))
    v = np.zeros((n , n,n ))

    x, y,z = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n),np.linspace(0,1,n))

    mask = (0.4 < x) & (x < 0.6) & (0.4 < y) & (y < 0.6) & (0.4 < z) & (z < 0.6)

    u[mask] = 0.50
    v[mask] = 0.25
    return u,v

#U, V = init_StateRand()
U,V=init(size)
W=np.zeros([size, size, size])
#W[0:10,20:30,40:50]=1

def laplacian(Z):  # newtnova metoda laplacian
    Ztop = Z[1:-1, 0:-2, 1:-1]  # +y _,_,_
    Zleft = Z[1:-1, 1:-1, 0:-2]  # -x
    Zbottom = Z[1:-1, 2:, 1:-1]  # -y
    Zright = Z[1:-1, 1:-1, 2:]  # +x
    Zcenter = Z[1:-1, 1:-1, 1:-1]  # c
    Zup = Z[0:-2, 1:-1, 1:-1]  # +z
    Zdown = Z[2:, 1:-1, 1:-1]  # -z
    try:
        return (Ztop + Zleft + Zbottom + Zright + Zup + Zdown -
                6 * Zcenter)
    except:
        print("test")

import random
step_plot = n // 9
# We simulate the PDE with the finite difference
u = []
w = []

Du, Dv = .1, .05
F, k = 0.0545, 0.062

for i in range(n):
    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)

    # We take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1, 1:-1]
    Vc = V[1:-1, 1:-1, 1:-1]
    Wc = W[1:-1, 1:-1, 1:-1]
    # We update the variables.
    uvv = Uc * Vc * Vc
    U[1:-1, 1:-1,1:-1], V[1:-1, 1:-1,1:-1] = Uc+ Du * deltaU - uvv + F * (1 - Uc),Vc + Dv * deltaV + uvv - (F + k) * Vc

    #    Uc + dt * (-Uc * (-deltaU)**(epsilon/2) + b*(a/b-Uc)-b1*Vc**2*Uc), \
    #    Vc + dt * (-Vc * (-deltaV)**(epsilon/2) +b2*Vc+b1*Vc**2*Uc )
   # print((b2*Vc).shape)
    #print(Wc.shape)
    W[1:-1, 1:-1, 1:-1]=Wc+b2*Vc+0.1*random.random()*Vc
    #print(W)
    # Neumann cododanditions: derivatives at the edges
    # are null.
    for Z in (U, V,W):
        Z[:, 0, :] = Z[:, 1, :]
        Z[:, -1, :] = Z[:, -2, :]
        Z[:, :, 0] = Z[:, :, 1]
        Z[:, :, -1] = Z[:, :, -2]
        Z[0, :, :] = Z[1, :, :]
        Z[-1, :, :] = Z[-2, :, :]
    # We plot the state of the system at
    # 9 different times.
    if (i == 8000):
        break;
    # if i % step_plot == 0 and i < 9 * step_plot:
    u.append(np.copy(W))
    #w.append(np.copy(W))
    print(i)

import vizualize3d as vz3D
u=u[-3:-1]
print(len(u))
vz3D.init(u)
vz3D.start()

# fig, ax = plt.subplots(1, 1, figsize=(8, 8))
# show_patterns(U, ax=ax)
# plt.show()
# print(u)

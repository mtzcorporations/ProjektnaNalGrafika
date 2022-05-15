

from math import *
import timeit
start = timeit.default_timer()
import numpy as np
import vizualize3d as vz3D
import random

size =100


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

    mask = (x**2 + y**2 + z**2 > 0.4) & (x**2 + y**2+z**2 < 0.45) & (z > 0) & (z< 0.3) &(y > 0.3) & (y< 0.5) & (x > 0.3) & (x< 0.6)
    mask2=np.copy(mask)

    u[mask] = 0.50
    v[mask2] = 0.25
    #v[-100:-50, :, :] = 0
    #u[-100:-80, -100:20, -80:-60] = 0
    return u,v
def matrixOFdistance():
    center=[20,50,50]
    maxDist=0.0001
    matrix=np.zeros([size, size, size])
    for x in range(size):
        for y in range(size):
            for z in range(size):
                distance=math.sqrt((x-center[2])**2+(y-center[1])**2+(z-center[0])**2)
                if distance>maxDist:
                    maxDist=distance
                matrix[z,y,x]=distance
    return matrix/maxDist

U,V=init(size)
#W=np.copy(V)
W=np.zeros([size, size, size])



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



def runSimulation(U,V,W):
    u = []
    Du, Dv = .1, .05
    F, k = 0.0545, 0.062
    n=1000
    for i in range(n):

        deltaU = laplacian(U)
        deltaV = laplacian(V)


        Uc = U[1:-1, 1:-1, 1:-1]
        Vc = V[1:-1, 1:-1, 1:-1]
        Wc = W[1:-1, 1:-1, 1:-1]
        #  update the variables.
        uvv = Uc * Vc * Vc
        U[1:-1, 1:-1,1:-1], V[1:-1, 1:-1,1:-1] = Uc+ Du * deltaU - uvv + F * (1 - Uc),Vc + Dv * deltaV + uvv - (F + k) * Vc
        #F=F+0.00017
        #k=k+0.00013
        #    Uc + dt * (-Uc * (-deltaU)**(epsilon/2) + b*(a/b-Uc)-b1*Vc**2*Uc), \
        #    Vc + dt * (-Vc * (-deltaV)**(epsilon/2) +b2*Vc+b1*Vc**2*Uc )
       # print((b2*Vc).shape)
        #print(Wc.shape)
        W[1:-1, 1:-1, 1:-1]=Wc+Vc #0.1*random.random()*Vc
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
        if(i%20==0):
            u.append(np.copy(W))
        # 9 different times.
        if (i == n-1):
            u.append(np.copy(W))
            break;
        # if i % step_plot == 0 and i < 9 * step_plot:

        format_float = "{:.2f}".format(i / n * 100)
        print(format_float, "%")
    return u

u=runSimulation(U,V,W)
stop = timeit.default_timer()
print('Time: ', stop - start)
vz3D.init(u)
vz3D.start()

# fig, ax = plt.subplots(1, 1, figsize=(8, 8))
# show_patterns(U, ax=ax)
# plt.show()
# print(u)
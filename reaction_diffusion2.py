import numpy as np
#import matplotlib.pyplot as plt


a = 2.8e-6
b = 5e-5
tau = .001
k = -.00005

size = 100  # size of the 2D grid
dx = 2. / size  # space step
T = 9.0  # total time
dt = .00005  # time step
n = int(T / dt)  # number of iterations

U = np.random.rand(size, size,size)
V = np.random.rand(size, size,size)

def laplacian(Z): #sobel , ker je ta občutljiva na šum #pretvori v 3kotniški model-marching cubes
    Ztop =    Z[1:-1,0:-2, 1:-1] # +y _,_,_
    Zleft =   Z[1:-1,1:-1, 0:-2] # -x
    Zbottom = Z[1:-1,2: ,1:-1] # -y
    Zright =  Z[1:-1,1:-1,2: ] # +x
    Zcenter = Z[1:-1,1:-1,1:-1] # c
    Zup =     Z[0:-2,1:-1,1:-1] # +z
    Zdown =   Z[2:  ,1:-1,1:-1] # -z
    try:
        return (Ztop + Zleft + Zbottom + Zright + Zup + Zdown -
            6 * Zcenter) / dx ** 3
    except:
        print("test")



step_plot = n // 9
# We simulate the PDE with the finite difference
u=[]
for i in range(n):
    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)

    # We take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1,1:-1]
    Vc = V[1:-1, 1:-1,1:-1]
    # We update the variables.
    U[1:-1, 1:-1,1:-1], V[1:-1, 1:-1,1:-1] = \
        Uc + dt * (a * deltaU + Uc - Uc ** 3 - Vc + k), \
        Vc + dt * (b * deltaV + Uc - Vc) / tau
    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[:,0, :] = Z[:,1, :]
        Z[:,-1, :] = Z[:,-2, :]
        Z[:,:, 0] = Z[:, :,1]
        Z[:,:, -1] = Z[:,:, -2]
        Z[0, :, :] = Z[1, :, :]
        Z[-1, :, :] = Z[-2, :, :]
    # We plot the state of the system at
    # 9 different times.
    if (i == 20):
        break;
    #if i % step_plot == 0 and i < 9 * step_plot:
    u.append(np.copy(U))
    print(i)

import vizualize3d as vz3D
vz3D.init(u)
vz3D.start()


#fig, ax = plt.subplots(1, 1, figsize=(8, 8))
#show_patterns(U, ax=ax)
#plt.show()
#print(u)

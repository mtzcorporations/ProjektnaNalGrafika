import numpy as np

m=np.array([[1,2,3,4,5,6],[7,8,9,10,11,12],[10,20,30,40,50,60],[70,80,90,100,110,120],
            [210,220,230,240,250,260],[270,280,290,2100,2110,2120]]) #2d
print(m[0:-2,1:-1])

def laplacian(Z):
    global dx
    Ztop = Z[1:-1,0:-2, 1:-1] # +y _,_,_
    Zleft = Z[1:-1,1:-1, 0:-2] # -x
    Zbottom = Z[1:-1,2:, 1:-1] # -y
    Zright = Z[1:-1,1:-1, 2:] # +x
    Zcenter = Z[1:-1,1:-1, 1:-1] #c
    Zup = Z[0:-2,1:-1,1:-1]
    Zdown = Z[2:, 1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright + Zup + Zdown -
            6 * Zcenter) / dx ** 3
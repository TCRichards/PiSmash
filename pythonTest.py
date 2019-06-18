import numpy as np
import matplotlib.pyplot as plt

R = 3.9
rho = 142
r = 0.815
numCells = 25

#============Functions
def a(x):
    return ((2*rho) + (x*R)) / ((2*rho) + (x*(R+r)))

def b(x):
    return ((rho) + (x*R))/((2*rho) + (x*(R+r)))
#============
cells = np.arange(0,numCells,1) # Create a list from 0 to numCells
sums = np.zeros(numCells)
functions = np.empty((numCells), dtype = 'object')


for i in range(numCells):
    if i == 0:
        functions[i] = 1
    elif i == 1:
        functions[i] = 'a(x)'
        prev = 'a(x)'
    else:
        functions[i] = '1.0-'+prev+')*b(x-'+str(i-1)+')'
        prev = '1.0-'+prev+')*b(x-'+str(i-1)+')'

plt.plot(cells, a(cells), label='a(x)')
plt.plot(cells, b(cells), label='b(x)')
plt.legend()
plt.show()

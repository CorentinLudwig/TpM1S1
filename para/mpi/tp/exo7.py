import numpy as np
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    Soluce = np.zeros(size,dtype='i')
else:
    Soluce = None

nb = 100000
inside = 0
np.random.seed(42*rank)

start_time = time.time()
for _ in range(nb//size):
    x = random.random()
    y = random.random()
    if x*x + y*y <= 1:
        inside +=1

A = np.zeros(1,dtype='i')
A[0] = inside

comm.Gather(A,Soluce,root=0)

if rank==0:
    print(Soluce)
    end_time = time.time()
    print("Pi =", 4 * Soluce.sum()/nb, "in ", end_time-start_time, 'seconds')
import numpy as np
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = 2
N = 10

if rank == 0:
    # To simulate we read the matrix from a file
    np.random.seed(10)
    A = np.random.rand(N,N)
else:
    A = np.zeros((N,N))



local_a = rank * size
local_b = (rank+1) * size
# Need a copy not a pointer on the same array
res = A.copy()
for _ in range(n-1):
    tmp = np.zeros((N, N))
    for lin in range(N):
        for col in range(local_a,local_b):
            for i in range(N):
                tmp[lin][col] += A[lin][i] * res[i][col]
    res = tmp.copy()

print('Signature    ', res.trace())


from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    passnumber=np.array([42])
else:
    passnumber = np.array([0])

print("At start in process of rank",rank," the passnumber is ",passnumber[0])

comm.Bcast(passnumber,root=0)

print("After collective in process of rank ",rank," the passnumber is ",passnumber[0])
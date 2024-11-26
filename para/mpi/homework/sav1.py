# python3 n-bodies-base.py 12 1000

import sys
import time
import random
import numpy as np
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE
from n_bodies import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()



nbbodies = int(sys.argv[1])
NBSTEPS = int(sys.argv[2])
DISPLAY = len(sys.argv) != 4


start_time = time.time()

# Modify only starting here
if rank == 0:
    data = init_world(nbbodies)
    local_size = np.array([nbbodies/size],dtype=int)
else:
    data = None
    local_size = np.empty(1,dtype=int)

comm.Bcast(local_size, root=0)

local_size = local_size[0]

data_compute = np.empty((local_size,6),dtype=float)


local_data = None

for t in range(NBSTEPS):
    comm.Scatter(data,data_compute,root=0)
    force = np.zeros((local_size,2))
    for i in range(local_size):
        for s in range(size):
            if rank == 0:
                local_data = data[s*local_size:(s+1)*local_size]
            comm.Bcast(local_data,root=0)
            for j in range(local_size):
                force[i] = force[i] + interaction(data_compute[i],local_data[j])
    
    for i in range(local_size):
        data_compute[i] = update(data[i], force[i])
    comm.AllGather(data_compute,data,root=0)




end_time = time.time()   
print("Duration:", end_time-start_time)
print("Signature: %.4e" % (signature(data)))
print("Unbalance: %d" % (100*(0)))
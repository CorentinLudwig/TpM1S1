import numpy as np
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

SIZE = 20

def get_max(tab):
    pos = np.argmax(tab)
    return [tab[pos],pos]

#np.random.seed(42)

if rank==0:
    tab = np.random.randint(100, size = SIZE, dtype='i')
    tab_max = np.zeros(size,dtype='i')
    tab_max_index = np.zeros(size,dtype='i')
    print(tab)
else:
    tab = None
    tab_max = None
    tab_max_index = None


local_size = SIZE//size
local_tab=np.zeros(local_size,dtype='i')
comm.Scatter(tab,local_tab,root=0)

soluce = get_max(local_tab)

comm.Gather(np.array(soluce[0]),tab_max,root=0)
comm.Gather(np.array(soluce[1]+rank*local_size),SIZE//size//size_index,root=0)

if(rank == 0):
    max,i_max = get_max(tab_max)
    print(tab_max_idex[i_max])
    if(tab_max_idex[i_max] == np.argmax(tab)):
        print("Succed")


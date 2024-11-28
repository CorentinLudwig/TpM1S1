import sys
import time
import numpy as np
from mpi4py import MPI
from n_bodies import init_world, interaction, update, signature, displayPlot

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Input parameters
nbbodies = int(sys.argv[1])
NBSTEPS = int(sys.argv[2])
DISPLAY = len(sys.argv) != 4

# Timing
start_time = time.time()

# Initialize data on the root process
if rank == 0:
    data = init_world(nbbodies)
else:
    data = np.zeros((nbbodies, 6), dtype='f')

# Determine local size for each process
local_size = nbbodies // size


# Simulation loop
data_update=np.zeros((local_size,6), dtype='f')
interaction_use = 0
for t in range(NBSTEPS):
    comm.Bcast(data, root=0)
    # calcule the force for all bodies
    force = np.zeros((nbbodies, 2), dtype='f')
    for i in range(local_size):
        i_global = i+rank*local_size
        for j in range(i_global):
            force_j_on_i = interaction(data[i_global], data[j])
            force[i_global] += force_j_on_i
            force[j] -= force_j_on_i
            interaction_use += 1

    force_compute = np.zeros((nbbodies, 2), dtype='f')
    comm.Reduce(force,force_compute,op=MPI.SUM,root=0)
    
    if rank==0:
        #update all bodies
        for i in range(nbbodies):
            data[i] = update(data[i], force_compute[i])
            
# calcule of unbalance
interaction_use = np.array([interaction_use])

if rank == 0:
    unbalance_tab = np.zeros(size,dtype=int)
else:
    unbalance_tab = None

comm.Gather(interaction_use,unbalance_tab, root=0)

if rank == 0:
    unbalance = 100 * ((unbalance_tab.max()-unbalance_tab.min())/unbalance_tab.sum())

    end_time = time.time()
    # Output results
    print("Duration:", end_time - start_time)
    print("Signature: %.4e" % signature(data))
    print("Unbalance: %d" % (unbalance))

    # Display the results if requested
    if DISPLAY:
        displayPlot(data)

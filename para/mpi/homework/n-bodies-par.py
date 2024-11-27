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


# Broadcast initial data to all processes
comm.Bcast(data, root=0)

# Simulation loop
for t in range(NBSTEPS):

    # Compute forces
    force = np.zeros((local_size, 2))
    for i in range(local_size):
        for j in range(nbbodies):
            force[i] += interaction(data[i], data[j])

    # Update positions and 
    data_update=np.zeros((local_size,6), dtype='f')
    for i in range(local_size):
        data_update[i] = update(data[i], force[i])
    
    comm.Allgather(data_update,data)

    # Gather updated data from all processes
    data = np.zeros((nbbodies, 6), dtype='f')
    comm.Gather(data_update, data, root=0)

    # Optionally broadcast the updated global data back to all processes
    if t < NBSTEPS - 1:  # Skip on the last step as no further computation follows
        comm.Bcast(data, root=0)

# Finalize timing
end_time = time.time()

# Output results
if rank == 0:
    print("Duration:", end_time - start_time)
    print("Signature: %.4e" % signature(data))
    print("Unbalance: %d" % (100 * (0)))  # Placeholder for unbalance computation

    # Display the results if requested
    if DISPLAY:
        displayPlot(data)

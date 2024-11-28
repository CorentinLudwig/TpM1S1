import sys
import time
import random
import numpy as np

from n_bodies import *

nbbodies = int(sys.argv[1])
NBSTEPS = int(sys.argv[2])
DISPLAY = len(sys.argv) != 4

start_time = time.time()


data = init_world(nbbodies)


# Simulation loop
for t in range(NBSTEPS):
    # calcule the force for all bodies
    force = np.zeros((nbbodies,2))
    for i in range(nbbodies):
        for j in range(nbbodies):
            force[i] = force[i] + interaction(data[i],data[j])
    
    #update all bodies
    for i in range(nbbodies):
        data[i] = update(data[i], force[i])
    
    if DISPLAY:
        displayPlot(data)




end_time = time.time()

# Output results
print("Duration:", end_time-start_time)
print("Signature: %.4e" % (signature(data)))
print("Unbalance: %d" % (100*(0)))
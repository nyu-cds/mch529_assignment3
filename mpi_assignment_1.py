import numpy
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcesses = comm.Get_size()
if rank % 2 ==0:
        print("hello from process " + str(rank))
        
        
if rank % 2 ==1:
        print("goodbye from process " +  str(rank))

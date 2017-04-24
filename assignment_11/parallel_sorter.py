"""
Michael Higgins (mch529)

This is a sorter that parallelizes the job between X processes.  X is 
determined by running the command mpiexec -n X python parallel_sorter.py

The user is then asked to pick a positive whole number that will be the number
of numbers to be sorted. They are reprompted if they make a mistake in entry.



"""

import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
num_processes = comm.Get_size()


def check_sorted(sorted_list):
    """
    input: list of numbers
    output: boolean indicating whether or not the list is in increasing order
    """
    differences = np.array([sorted_list[i] - sorted_list[i+1 ] for i in range(len(sorted_list)-1) ])
    return np.all(differences <= 0)

def split_into_chunks(ints, num_buckets):
    """
    input: array of numbers
    ouput: list of num_buckets lists.  Sublist i has contains numbers in ints 
    within the range [min(ints)+i*(max - min)/num_buckets , min(ints)+(i+1)*(max - min)/num_buckets )
    """
    maximum = np.max(ints) 
    minimum = np.min(ints)
    # find smallest and largest values for each bin
    bins = np.linspace(minimum,maximum, num_buckets + 1 )
    
    # seperate into evenly spaced chunks
    chunks = [  ints[ np.logical_and( (ints >= bins[i]) , (ints < bins[i+1]))] for i in range(len(bins)-1) ]
    
    # need to include very last number into last list as many times as it occurs
    chunks[-1] = np.concatenate([chunks[-1], ints[ints == maximum]],axis =0)
    return chunks

if rank ==0:
    # handle input
    #make 10000 random numbers between 0 and 1000
    random_numbers = np.random.randint(0,1000,2000)
    chunks =  split_into_chunks(random_numbers, num_processes)
    
else:
    chunks = None

# send data to all other processes    
chunk = comm.scatter(chunks,root=0)

#sort smaller chunks based on process
chunk = np.sort(chunk)

# gather all the sorted chunks
sorted_chunks = comm.gather(chunk,root=0)

if rank ==0:
    # make list of list flat
    # taken from http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    sorted_chunks = [item for sublist in sorted_chunks for item in sublist]
    
    #check to make sure sorted list is same as original numbers and that they are non-decreasing
    if not check_sorted(sorted_chunks) :
        print("something went horribly wrong!!!!!")
    
    if  len(sorted_chunks) != len(random_numbers):
        print("wrong size")
        
    else:
        print("success!")
        print(sorted_chunks)

    
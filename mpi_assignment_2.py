"""
to run type: mpi4exec -n {how many processes you want} mpi_assignment_1.py

compute {how many processes you want}*user_input!  
user_input is a whole number between 0 and 100 that is typed into the command line.

Works by inputing and verifying input in process 0, sending input to 1, which 
multiplies input by 1, sends that value to process to 2, which multiples that 
value by 3 and so on until the last process which sends the value back to 
process 0 which then prints the resulting value.

"""
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
numProcesses = comm.Get_size()

if rank ==0:

	while True:
		try:
			data = input('type an integer less than 100 and greater than 0: ')  
			# checks if its  an int 
			int(data)
		except :
			print("not an int, try again")
			continue

		#now its okay to convert from string to int
		data =int(data)
		if  data >100 or data < 1 :
			data = input("Not between 0 and 100, try again ")
		else:
			break
	# data is confirmed send to next process
	comm.send(data, dest=1 )
	# get data and print from last process
	data = comm.recv( source = numProcesses - 1  )
	print(data)

else:
	data = comm.recv( source=rank-1 )
	data =data*rank
	comm.send(data  , (rank+1) % numProcesses )
import itertools 

def zbits(n,k):
	"""
	returns set of all binary strings of length n that contain k zero bits
	n and k must be positive integers
	
	"""
	# tests to make sure input is good
	assert (type(n)==int) and (type(k)==int), "Inputs must be integers"
	assert (n>=0) and (k>=0), "Inputs must be positive"
	assert k<=n, "k must be less than or equal to n"


	zeroes = itertools.repeat('0',k)
	ones = itertools.repeat('1',n-k)
	# make a string a tuple of k 0's , n-k 1's
	zeroesAndOnes = itertools.chain(zeroes , ones)

	# turn from tuple to string using join, get permutations of zeroesAndOnes
	return {"".join(thing) for thing in itertools.permutations(zeroesAndOnes)}


if __name__ == '__main__':
	assert zbits(4, 3) == {'0100', '0001', '0010', '1000'}, "failed first test"
	assert zbits(4, 1) == {'0111', '1011', '1101', '1110'}, 'failed second test'
	assert zbits(5, 4) == {'00001', '00100', '01000', '10000', '00010'}, 'failed third'


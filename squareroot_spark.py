
"""
Michael Higgins (mch529)

computes (sqrt(1) +...+ sqrt(1000))/1000 utilizing spark parallelize and fold method.  
Also uses map,lambda to perfrom sqrt operation
"""
from pyspark import SparkContext

def add(a,b):
	return a+b
if __name__ == '__main__':
	sc = SparkContext("local", "factorial")
	# Create an RDD of numbers from 1 to 10000 and then product of those numbers
	nums = sc.parallelize(range(1,1001))
	square_roots = nums.map(lambda x: x**.5)
	sum_square_roots= square_roots.fold(0,add)
	
	print("sum_square_roots",sum_square_roots/1000.)
    
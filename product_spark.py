"""
Michael Higgins
mch529

Computes 1000! utilizing spark parallelize and fold methods
"""

from pyspark import SparkContext

def multiply(a,b):
    """
    Given two numbers a,b returns the product a*b
    """
    return a*b

if __name__ == '__main__':
	sc = SparkContext("local", "factorial")
	# Create an RDD of numbers from 1 to 10000 and then product of those numbers
	nums = sc.parallelize(range(1,1001)).fold(1,multiply)
	
	print("1000! = ",nums)
    
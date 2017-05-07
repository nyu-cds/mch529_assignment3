
"""
Michael Higgins (mch529)

Calculates number of distinct words in document utilizing spark map/reduce.
"""

from pyspark import SparkContext
import re

# remove any non-words and split lines into separate words
# finally, convert all words to lowercase
def splitter(line):
    line = re.sub(r'^\W+|\W+$', '', line)
    return map(str.lower, re.split(r'\W+', line))


if __name__ == '__main__':

	# configuration
	sc = SparkContext("local", "words")

	text = sc.textFile('/home/owner/Downloads/spark-1.6.0/bin/pg2701.txt')
	words = text.flatMap(splitter)
	words_mapped = words.map(lambda x: (x, 1))

	# count the number of distinct words
	# distinct_words = words_mapped.keys().distinct().count()
	# print("The number of distinct words: ", distinct_words)

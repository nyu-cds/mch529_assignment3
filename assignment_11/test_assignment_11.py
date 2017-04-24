"""
Michael Higgins 
mch529

Test functionality of parallel_sorter.py

"""

import unittest
import parallel_sorter 
import numpy as np

class Test(unittest.TestCase):

    def test_check_sorted(self):
        # for 100 different list sizes in [1,5000] verify that check_sorted is working
        for i in range(100):
            num_ints = np.random.randint(1,5000,1)[0]
            unsorted_list = np.random.randint(1,1000, num_ints)
            assert parallel_sorter.check_sorted(np.sort(unsorted_list)) ==True
    
    def test_split_into_chunks(self):
        """
        simple test to see if split_into_chunks is putting numbers in proper buckets
        """
        check_list =np.arange(10)
        bins = split_into_chunks(check_list, 2)
        print (bins[0] == np.arange(50))
        assert len(bins)==2
        assert np.all(bins[0] == np.arange(5))
        assert np.all(bins[1] == np.arange(5,10))

        
if __name__ == '__main__':
    unittest.main()
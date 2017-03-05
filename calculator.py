# -----------------------------------------------------------------------------
# calculator.py
# ----------------------------------------------------------------------------- 

# old time = 1.18
# new time = .003
# speed up ratio = 1.18/.03 =39.3

# I used ipython notebook commands %prun and %timeit to analyze line speeds/overall time.  
# I chose to use numpy to replace these operations as they are
# already optimized for these kinds of operations.



import numpy as np
import numpy as np
import calculator as calc
def add(x,y):
    """
    Add two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    
    return np.add(x, y)


def multiply(x,y):
    """
    Multiply two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    return np.multiply(x,y)

def sqrt(x):
    """
    Take the square root of the elements of an arrays using a Python loop.
    """
    return np.sqrt(x)


def hypotenuse(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = multiply(x,x)
    yy = multiply(y,y)
    zz = add(xx, yy)
    return sqrt(zz)

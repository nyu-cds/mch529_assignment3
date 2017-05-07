#
# Simple Python program to calculate elements in the Mandelbrot set.
#
import numpy as np
from pylab import imshow, show
from numba import cuda
print(cuda.gpus)
#==============================================================================
#  
# @cuda.jit
# def mandel(x, y, max_iters):
#     '''
#     Given the real and imaginary parts of a complex number,
#     determine if it is a candidate for membership in the 
#     Mandelbrot set given a fixed number of iterations.
#     '''
#     c = complex(x, y)
#     z = 0.0j
#     for i in range(max_iters):
#         z = z*z + c
#         if (z.real*z.real + z.imag*z.imag) >= 4:
#             return i
#             
#     return max_iters
# 
# @cuda.jit
# def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
#     '''
# 	Calculate the mandel value for each element in the 
# 	image array. The real and imag variables contain a 
# 	value for each element of the complex space defined 
# 	by the X and Y boundaries (min_x, max_x) and 
# 	(min_y, max_y).
#     '''
#     height = image.shape[0]
#     width = image.shape[1]
#     
#     pixel_size_x = (max_x - min_x) / width
#     pixel_size_y = (max_y - min_y) / height
#     
#     block_w, block_h = cuda.blockDim.x, cuda.blockDim.y
#     print(block_w)
# #==============================================================================
# #     
# #     for x in range(width):
# #         real = min_x + x * pixel_size_x
# #         for y in range(height):
# #             imag = min_y + y * pixel_size_y
# #             image[y, x] = mandel(real, imag, iters)
# #==============================================================================
#             
# if __name__ == '__main__':
# 	image = np.zeros((1024, 1536), dtype = np.uint8)
# 	compute_mandel(-2.0, 1.0, -1.0, 1.0, image, 20) 
# 	imshow(image)
# 	show()
#==============================================================================

#
# Simple Python program to calculate elements in the Mandelbrot set.
#
import numpy as np
from numba import cuda
from pylab import imshow, show
import math


xvals =[]
@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
        Given the real and imaginary parts of a complex number,
        determine if it is a candidate for membership in the
        Mandelbrot set given a fixed number of iterations.
        '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

@cuda.jit()
def compute_mandel(min_x, max_x, min_y, max_y, image, iters  ):
    '''
        Calculate the mandel value for each element in the
        image array. The real and imag variables contain a
        value for each element of the complex space defined
        by the X and Y boundaries (min_x, max_x) and
        (min_y, max_y).
    block of image is computed for each call of this function. If block_dim = (a,b)
    grid_dim = (c,d) then this function is called a*b*c*d times.  The dimension of each block
    is given by ceil(image[0]/ac) by  ceil(image[1]/bd).  Each value of that block
    is calculated within this function.
    '''
    height = image.shape[0]
    width = image.shape[1]
    
    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
                   
    block_id_x, block_id_y = cuda.grid(2)
    
    num_block_x = block_dim[0]*grid_dim[0]
    num_block_y = block_dim[1]*grid_dim[1]
    
    pixels_per_block_x = math.floor(width/(1.0*num_block_x))
    pixels_per_block_y = math.floor(height/(1.0*num_block_y))

    #print(pixels_per_block_x,pixels_per_block_y)

    start_pixel_x = block_id_x * pixels_per_block_x
    start_pixel_y = block_id_y * pixels_per_block_y
    
    pixels_x = range(start_pixel_x,start_pixel_x + pixels_per_block_x )
    pixels_y = range(start_pixel_y,start_pixel_y + pixels_per_block_y )

    
    for i in pixels_x:
        real = min_x + i*pixel_size_x
        for j in pixels_y:
            imag =  min_y + j*pixel_size_y
            #image[i,j]= 100
            #if j<height and i < width:
            #image[j,i]= mandel(real,imag, iters) 
            
if __name__ == '__main__':
    image_w, image_h =1024,1536
    
    block_dim = (32, 8)
    grid_dim = (32, 16)

    image = np.zeros((image_w, image_h), dtype = np.uint8)
    
    image_global_mem = cuda.to_device(image)
    compute_mandel[grid_dim, block_dim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 10 )
    image_global_mem.copy_to_host()
    imshow(image)
    show()


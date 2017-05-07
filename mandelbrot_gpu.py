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
    
    #get block absolute indexes 
    block_id_x, block_id_y = cuda.grid(2)
    
    num_block_x = block_dim[0]*grid_dim[0]
    num_block_y = block_dim[1]*grid_dim[1]
    
    #divide blocks evenly among pixels
    pixels_per_block_x = math.ceil(width/(1.0*num_block_x))
    pixels_per_block_y = math.ceil(height/(1.0*num_block_y))

    #find upper lhs of relative pixel (0,0) for this block
    start_pixel_x = block_id_x * pixels_per_block_x
    start_pixel_y = block_id_y * pixels_per_block_y
    
    # only calculate for this block
    pixels_x = range(start_pixel_x,start_pixel_x + pixels_per_block_x )
    pixels_y = range(start_pixel_y,start_pixel_y + pixels_per_block_y )

    
    for i in pixels_x:
        real = min_x + i*pixel_size_x
        for j in pixels_y:
            imag =  min_y + j*pixel_size_y
            if j<height and i < width:
                image[j,i]= mandel(real,imag, iters) 
            
if __name__ == '__main__':
    image_w, image_h =1024,1536
    
    block_dim = (32, 16)
    grid_dim = (32, 16)

    image = np.zeros((image_w, image_h), dtype = np.uint8)
    
    image_global_mem = cuda.to_device(image)
    compute_mandel[block_dim, grid_dim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 30 )
    image_global_mem.copy_to_host()
    imshow(image)
    show()

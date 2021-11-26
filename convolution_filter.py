""" SYSC 1005 Fall 2014 - Matrix convolution and image processing.

A convolution kernel is a square matrix; for example:

    |c00  c01  c02|
C = |c10  c11  c12|
    |c20  c21  c22|

In the example, the kernel is a 3-by-3 matrix, but it could be larger 
(e.g., 5-by-5, 7-by-7, etc.)

The element at the center of the matrix is known as the anchor point.

Here is a 3-by-3 region in the upper-left corner of an image.

  (r1, g1, b1)  (r2, g2, b2)  (r3, g3, b3)  ...  ...
  (r4, g4, b4)  (r5, g5, b5)  (r6, g6, b6)  ...  ...
  (r7, g7, b7)  (r8, g8, b8)  (r9, g9, b9)  ...  ...
       ...           ...           ...      ...  ...
       ...           ...           ...      ...  ...

(r1, b1, g1) represent the red, green and blue components of the pixel in
the upper-left corner; (r2, g2, b2) represent the red, green and blue
components of the pixel to the right of it, etc.

The convolution kernel is placed over the square region in the image. Note that
the kernel's anchor point will be above the pixel in the center of the region;
i.e., (r5, g5, b5).

Each element in the convolution kernel is multiplied by the red component of
the pixel beneath it, and these products are added together. This sum is
divided by the sum of the elements in the kernel. This value will be
used as the red component for the new colour for the pixel under the anchor
point.

In other words, when the anchor point is placed over the pixel with colour 
(r5, g5, b5),

kernel_sum = c00 + c01 + c02 + c10 + c11 + c12 + c20 + c21 + c22

new_red = (c00 * r1 + c01 * r2 + c02 * r3 +
           c10 * r4 + c11 * r5 + c12 * r6 +
           c20 * r7 + c21 * r8 + c22 * r9) // kernel_sum

The convolution is repeated for the green and blue components in the region.

After the new red, green and blue components have been calculated, the
pixel's new colour is calculated.

We then shift the convolution kernel one pixel to the right, and repeat the
convolution. After processing one row, we shift the kernel down to the next row.
"""

from Cimpl import *

def convolution_filter(img, kernels, name):
    dest = create_image(get_width(img), get_height(img))
    kernel=kernels[name]
    for y in range(1, get_height(img)-1):
        for x in range(1, get_width(img)-1):
            
            sum_red = 0
            sum_green = 0
            sum_blue = 0
            divisor = 0

            # NW (north west corner)
            r, g, b = get_color(img, x-1, y-1)
            sum_red = sum_red + r * kernel[0][0] 
            sum_green = sum_green + g * kernel[0][0] 
            sum_blue = sum_blue + b * kernel[0][0]
            divisor = divisor + kernel[0][0] 

            # N
            r, g, b = get_color(img, x, y-1)
            sum_red = sum_red + r * kernel[0][1] 
            sum_green = sum_green + g * kernel[0][1] 
            sum_blue = sum_blue + b * kernel[0][1] 
            divisor = divisor + kernel[0][1]

            # NE
            r, g, b = get_color(img, x+1, y-1)
            sum_red = sum_red + r * kernel[0][2]
            sum_green = sum_green + g * kernel[0][2]
            sum_blue = sum_blue + b * kernel[0][2] 
            divisor = divisor + kernel[0][2]

            # W
            r, g, b = get_color(img, x-1, y)
            sum_red = sum_red + r * kernel[1][0]
            sum_green = sum_green + g * kernel[1][0] 
            sum_blue = sum_blue + b * kernel[1][0]
            divisor = divisor + kernel[1][0]

            # center
            r, g, b = get_color(img, x, y)
            sum_red = sum_red + r * kernel[1][1] 
            sum_green = sum_green + g * kernel[1][1] 
            sum_blue = sum_blue + b * kernel[1][1] 
            divisor = divisor + kernel[1][1] 

            # E
            r, g, b = get_color(img, x+1, y)
            sum_red = sum_red + r * kernel[1][2]
            sum_green = sum_green + g * kernel[1][2] 
            sum_blue = sum_blue + b * kernel[1][2] 
            divisor = divisor + kernel[1][2] 

            # SW
            r, g, b = get_color(img, x-1, y+1)
            sum_red = sum_red + r * kernel[2][0] 	
            sum_green = sum_green + g * kernel[2][0] 
            sum_blue = sum_blue + b * kernel[2][0]
            divisor = divisor + kernel[2][0] 
            
            # S
            r, g, b = get_color(img, x, y+1)
            sum_red = sum_red + r * kernel[2][1]
            sum_green = sum_green + g * kernel[2][1] 
            sum_blue = sum_blue + b * kernel[2][1] 
            divisor = divisor + kernel[2][1]

            # SE
            r, g, b = get_color(img, x+1, y+1)
            sum_red = sum_red + r * kernel[2][2] 
            sum_green = sum_green + g * kernel[2][2] 
            sum_blue = sum_blue + b * kernel[2][2] 
            divisor = divisor + kernel[2][2] 

            # To normalize the new component values, divide them by the sum
            # of the values in the kernel. If the divisor is 0, divide by 1.
            if divisor == 0:
                divisor = 1

            new_red = sum_red // divisor

            # Cimpl modifies components so that they lie between 0 and 255,
            # so we don't really need the next statement.
            new_red = min(max(new_red, 0), 255)

            new_green = sum_green // divisor
            new_green = min(max(new_green, 0), 255)
            
            new_blue = sum_blue // divisor
            new_blue = min(max(new_blue, 0), 255)
            
            col = create_color(new_red, new_green, new_blue)
            set_color(dest, x, y, col)

    # We've processed all the pixels except those on the edges.
    # Make those pixels black.

    black = create_color(0, 0, 0)

    bottom_row = get_height(img) - 1
    for x in range(get_width(img)):
        set_color(dest, x, 0, black)
        set_color(dest, x, bottom_row, black)

    right_column = get_width(img) - 1
    for y in range(get_height(img)):
        set_color(dest, 0, y, black)
        set_color(dest, right_column, y, black)

    return dest

blur_kernel = ((1, 1, 1),(1, 1, 1),(1, 1, 1))
sharpen_kernel = ((0, -3, 0),(-3, 21, -3),(0, -3, 0))
emboss_kernel = ((-18, -9, 0),(-9, 9, 9),(0, 9, 18))
edge_detect1_kernel = ((0, 9, 0),(9, -36, 9),(0, 9, 0))
edge_detect2_kernel = ((-9, -9, -9),(-9, 72, -9),(-9, -9, -9))

def build_kernel_table():
    return {'blur':blur_kernel,'sharpen':sharpen_kernel,'emboss':emboss_kernel,
        'edge detect 1':edge_detect1_kernel,'edge detect 2':edge_detect2_kernel}
    
def test_convolution_filter():
    img = load_image(choose_file())
    kernels=build_kernel_table()
    new_image = convolution_filter(img, kernels, name)
    show(new_image)
    # save_as(new_image, "convolution_blur.jpg")    

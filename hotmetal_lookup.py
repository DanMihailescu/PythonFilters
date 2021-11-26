from Cimpl import *

def solarize_table(threshold):
    lookup = []
    for c in range(256):
        if c < threshold:
            lookup.append(255 - c)
        else:
            lookup.append(c)
    return lookup

def build_hot_metal_lookup_table():
    table = []
    for n in range(0, 256):
        if n <= 170:
            r = 1.5*n
        else: 
            r = 255
        if n >= 170:
            g = 3*(n-170)
        else:
            g = 255
        col = create_color(r, g , 0)
        table.append(col)
    return table

hot_metal_table = build_hot_metal_lookup_table()

def hot_metal(img,table):
    for x, y, col in img: 
        r, g , b = col
        brightness = round(0.30*r+0.59*g+0.11*b)
        new_col = table[brightness]
        set_color(img, x, y, new_col)   
        
img=load_image(choose_file())
hot_metal(img,hot_metal_table)
show(img)